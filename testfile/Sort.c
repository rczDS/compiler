#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <string.h>
int main()
{
	char array_char[100];
	int array_int[100];
	for(int i=0;i<=99;++i)
	{
	    array_int[i]=0;
	    array_char[i]='\0';
	}


	gets(array_char);
	int i=0;
	int j=0;
	int k = 0;
	if (array_char[0] == '0')
	{
		printf("no data");
		return 0;
	}
	for (i = 0; i <= 99; i++)
	{
		if (array_char[i] == '\0')
		{	
			char temp[100];
			for(int i=0;i<=99;++i)
			{
			    temp[i]='\0';
			}

			int l = 0;
			while (j != i)
			{
				temp[l] = array_char[j];
				l = l + 1;
				j = j + 1;
			}
			array_int[k] = atoi(temp);

			j = j + 1;
			break;
			
		}
		else if (array_char[i] == ',')
		{
			char temp[100];
			for(int i=0;i<=99;++i)
			{
			    temp[i]='\0';
			}
			int l = 0;
			while (j != i)
			{

				temp[l] = array_char[j];
				l = l + 1;
				j = j + 1;
			}
			j = j + 1;
			array_int[k] = atoi(temp);

			k = k + 1;
		}
		
	}



	//sort
	for (int i = 0; i <= k; i++) 
	{
		for (int j = i; j > 0; j--) 
		{
			if (array_int[j] < array_int[j - 1])
			{
				int tmp;
				tmp = array_int[j];
				array_int[j] = array_int[j - 1];
				array_int[j - 1] = tmp;
			}
		}
	}
	for (int i = 0; i <= k; ++i)
	{
		printf("%d", array_int[i]);
		if(i!=k)
		{
		    printf(",");
		}

	}
}