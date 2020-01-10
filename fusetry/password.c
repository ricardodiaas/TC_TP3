#include<stdio.h>

#include<string.h>

int main()
{
    char studentID[]="admin", password[]="1234", id[20], p[20];
    int n=1, x, y, kk;

  
         printf("\nStudent_ID:");
         scanf("%s", &id);
         fflush(stdout);

         //printf("\nPassword:");
         //scanf("%s", &p);
         char pp = InputBox(0, "Please enter a value");
         printf("Value is %s.\n", pp);
         fflush(stdout);

         x=strcmp(id, studentID);
         y=strcmp(pp, password);

         if(x==0 && y==0){
           printf("\nSucessfully Logged In");
           kk = 1;
            //printf("%d",kk);
           return kk;
          
         }else {
           printf("\nWrong Password, try again", 5-n);
           kk = -1;
           //printf("%d",kk);
            return kk;
            n++;}

      

}