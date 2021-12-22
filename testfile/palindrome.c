#include <stdio.h>
#include <string.h>


int main() {
	printf("Please input a string:\n");
	char str[100];
	gets(str);
	int len = strlen(str);
	int flag = 0;
	for (int i = 0; i < len / 2; i++)
	{
		if (str[i] != str[len - 1 - i])
		{
			printf("No");
			flag = 1;
			break;
		}
	}
	if (!flag) printf("Yes");
	return 0;
}
