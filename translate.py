# coding=utf-8
import copy
from AST import ASTInternalNode, ASTExternalNode
from yacc import parser
from C_utils import c_utils
from pre_post_process import formatIndent, precompile

TAIL = """
if __name__ == "__main__":
    main_0()
"""


class Translator:
    def __init__(self):
        self.functions = []
        self.declarations = []
        self.global_variables = []
        self.variable_table = {}

        self.head = ""
        for c_util in c_utils:
            self.head += c_util
        self.head += '\n'
        self.tail = TAIL

        self.handle_function_dict = {
            "unary_expression": self.unary_expression_handler,
            "postfix_expression": self.postfix_expression_handler,
            'jump_statement': self.jump_statement_handler,
            'selection_statement': self.selection_statement_handler,
            'iteration_statement': self.iteration_statement_handler,
            'block_item_list': self.block_item_list_handler,
            'compound_statement': self.compound_statement_handler,
            'function_definition': self.function_definition_handler,
            'parameter_declaration': self.parameter_declaration_handler,
            'init_declarator_list': self.init_declarator_list_handler,
            'declaration': self.declaration_handler,
            'direct_declarator': self.direct_declarator_handler,
            'init_declarator': self.init_declarator_handler
        }

    def translate(self, input_file_name, output_file_name):
        try:
            # step0: input and preprocess
            success, file_content = precompile(input_file_name)
            if not success:
                print(file_content)
                return

            # step1,2: 词法语法处理
            tree = parser.parse(file_content)

            # step3: 语义处理
            raw_outcome = self.process(tree)

            # step4: 代码生成
            out = formatIndent(raw_outcome)
            out = self.head + out + self.tail

            # step5: output
            with open(output_file_name, 'w+', encoding='utf-8') as output_file:
                output_file.write(out)
            print('Compile success: {} -> {} '.format(input_file_name, output_file_name))
        except Exception as e:
            print(str(e))

    # 语义处理：按树形处理
    def process(self, tree):
        def pick_out(maintree):
            if maintree.key == 'function_definition':
                self.functions.append(maintree)
            else:
                self.declarations.append(maintree)

        # 分离函数和全局变量、结构体声明等
        while True:
            if tree.key == 'translation_unit':
                if len(tree.children) == 2:
                    pick_out(tree.children[1].children[0])
                    tree = tree.children[0]
                else:
                    pick_out(tree.children[0].children[0])
                    break

        self.declarations = reversed(self.declarations)
        code_list = []
        for declaration in self.declarations:
            self.declaration_extract(declaration)
            # print(declaration)

            code = self.traversal(declaration, [])
            code_list.extend(code)
            code_list.append('')
            # print(code)

        for function in self.functions:
            # 进入函数（作用域），备份变量表
            table_copy = copy.deepcopy(self.variable_table)
            self.rename(function)
            # 离开函数（作用域），恢复变量表
            self.variable_table = table_copy

            code = self.traversal(function, [])
            code_list.extend(code)
            code_list.append('')
        return code_list

    # get global var
    def declaration_extract(self, tree):
        # 外部节点直接返回
        if isinstance(tree, ASTExternalNode):
            return
        for child in tree.children:
            # 如果是变量
            if child.key == 'IDENTIFIER':
                # 在变量表中记录该变量
                alias = child.value + '_0'
                self.global_variables.append(alias)
                self.variable_table[child.value] = [(alias, True)]
                child.value = alias
            else:
                self.declaration_extract(child)

    # traverse the tree
    def traversal(self, tree, stack):
        stack.append(tree.key)
        code_list = []

        if isinstance(tree, ASTExternalNode):
            stack.pop()
            return self.leaf_string(tree)

        for child in tree.children:
            code = self.traversal(child, stack)
            code_list.append(code)

        pycode = self.code_compose(tree, code_list)

        stack.pop()
        return pycode

    # translate leaf val
    def leaf_string(self, tree):
        if tree.value == ';':
            return ['']
        elif tree.value == '&&':
            return [' and ']
        elif tree.value == '||':
            return [' or ']
        elif tree.value == '!':
            return ['not ']
        elif tree.value == 'true':
            return ['True']
        elif tree.value == 'false':
            return ['False']
        elif tree.value == '\'\\0\'':
            return ['None']
        else:
            return [tree.value]

    # rename
    def rename(self, tree, is_declarator=False):

        if isinstance(tree, ASTInternalNode):
            # 进入声明语句
            if tree.key == 'declarator':
                for child in tree.children:
                    self.rename(child, True)
            # 声明语句中的表达式部分不算声明
            elif tree.key == 'primary_expression':
                for child in tree.children:
                    self.rename(child, False)


            # 选择或循环语句，进入新一层作用域
            elif tree.key == 'iteration_statement' or tree.key == 'selection_statement':

                # 进入作用域，保存副本
                table_copy = copy.deepcopy(self.variable_table)
                for child in tree.children:
                    self.rename(child, is_declarator)
                # 离开作用域，恢复变量表
                self.variable_table = table_copy
            else:
                for child in tree.children:
                    self.rename(child, is_declarator)
        else:
            # 不是变量
            if tree.key != 'IDENTIFIER':
                return
            # 变量在变量表中
            if tree.value in self.variable_table.keys():
                # 是声明
                if is_declarator:
                    table = self.variable_table[tree.value]

                    # 需要重命名并修改变量表
                    alias = tree.value + '_' + str(len(table))
                    table.append((alias, False))
                    tree.value = alias
                # 不是声明
                else:
                    table = self.variable_table[tree.value]
                    # 需要重命名
                    if len(table) != 0:
                        last = table[-1][0]
                        tree.value = last

            else:
                alias = tree.value + '_0'
                self.variable_table[tree.value] = [(alias, False)]
                tree.value = alias

    # 具体转化：根据function表中处理
    def code_compose(self, tree, code_list):
        if tree.key in self.handle_function_dict:
            return self.code_generator(tree, code_list)
        else:
            return self.default_handler(tree, code_list)

    # ++x --x
    def unary_expression_handler(self, tree_node, code_list):
        if isinstance(tree_node.children[0], ASTExternalNode):
            if tree_node.children[0].value == '++':
                res = [code_list[1][0] + ' = ' + code_list[1][0] + '+1']

                return res
            if tree_node.children[0].value == '--':
                res = [code_list[1][0] + '=' + code_list[1][0] + '-1']

                return res
        else:
            return self.default_handler(tree_node, code_list)

    # x++ x--
    def postfix_expression_handler(self, tree_node, code_list):
        if len(tree_node.children) == 2:
            if tree_node.children[1].value == '--':
                res = [code_list[0][0] + '=' + code_list[0][0] + '-1']
                return res
            if tree_node.children[1].value == '++':
                res = [code_list[0][0] + '=' + code_list[0][0] + '+1']
                return res
        else:
            return self.default_handler(tree_node, code_list)

    # return
    def jump_statement_handler(self, tree_node, code_list):
        if tree_node.children[0].key == 'return':
            if len(tree_node.children) == 3:
                return [code_list[0][0] + ' ' + code_list[1][0]]
        else:
            return self.default_handler(tree_node, code_list)

    # if else
    def selection_statement_handler(self, tree_node, code_list):
        if len(tree_node.children) == 5:
            return ['if ' + code_list[2][0] + ':', code_list[4]]
        if len(tree_node.children) == 7:
            return ['if ' + code_list[2][0] + ':', code_list[4], 'else:', code_list[6]]
        else:
            return self.default_handler(tree_node, code_list)

    # while
    def iteration_statement_handler(self, tree_node, code_list):
        if tree_node.children[0].value == 'while':
            return ['while ' + code_list[2][0] + ':', code_list[4]]

        if len(tree_node.children) == 7:
            return [code_list[2][0], 'while ' + code_list[3][0] + ':', code_list[6], code_list[4]]

        else:
            return self.default_handler(tree_node, code_list)

    # 代码块
    def block_item_list_handler(self, tree_node, code_list):
        lst = []
        for code in code_list:
            for c in code:
                lst.append(c)
        return lst

    def compound_statement_handler(self, tree_node, code_list):
        if len(tree_node.children) == 3:
            return code_list[1]
        else:
            return self.default_handler(tree_node, code_list)

    def function_definition_handler(self, tree_node, code_list):
        if len(tree_node.children) == 3:
            function_body = []
            # 无脑加入所有全局变量
            for global_var in self.global_variables:
                function_body.append('global ' + global_var)
            for code in code_list[2]:
                function_body.append(code)

            return ['def ' + code_list[1][0] + ':',
                    function_body]
        else:
            return self.default_handler(tree_node, code_list)

    def parameter_declaration_handler(self, tree_node, code_list):
        if len(tree_node.children) == 2:
            return code_list[1]
        else:
            return self.default_handler(tree_node, code_list)

    def init_declarator_list_handler(self, tree_node, code_list):
        if len(tree_node.children) == 1:
            return code_list[0]
        else:
            return self.default_handler(tree_node, code_list)

    def declaration_handler(self, tree_node, code_list):
        if len(tree_node.children) == 3:
            return code_list[1]
        else:
            return self.default_handler(tree_node, code_list)

    def direct_declarator_handler(self, tree_node, code_list):
        if len(tree_node.children) == 4 and tree_node.children[2].key == 'assignment_expression' and tree_node.children[
            2].key == 'assignment_expression':
            return [code_list[0][0] + '=[' + 'None' + ']*' + code_list[2][0]]
        else:
            return self.default_handler(tree_node, code_list)

    def init_declarator_handler(self, tree_node, code_list):
        if len(tree_node.children) == 3 and code_list[0][0].find('[') >= 0:
            tmp = code_list[0][0]  # s[0]*5
            index_1 = tmp.find('[')
            left = tmp[:index_1 - 1]  # s
            length = code_list[0][0].split('*')[1]  # 5

        else:
            return self.default_handler(tree_node, code_list)

    def default_handler(self, tree_node, code_list):
        lst = []
        flag = True
        for code in code_list:
            if len(code) != 1:
                flag = False
        if flag:

            s = ''
            for code in code_list:
                s += code[0]
            lst.append(s)
        else:

            for code in code_list:
                lst.extend(code)
        return lst

    def code_generator(self, tree_node, code_list):
        if tree_node.key in self.handle_function_dict:
            return self.handle_function_dict[tree_node.key](tree_node, code_list)
        else:
            return self.default_handler(tree_node, code_list)
