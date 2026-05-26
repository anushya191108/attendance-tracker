#include<stdio.h>
int main()
{
    float fees;
    int i1,i2,i3,i4,i5,i6,bal;
    printf("fees details");
    printf("enter the name:shivesh");
printf("\n total fees :");
scanf("%f",&fees);
printf("\n enter the instalment1:");
scanf("%d",&i1);
bal=fees-i1;
printf("\n enter the instalment2:");
scanf("%d",&i2);
bal=fees-(i1+i2);
printf("\n enter the instalment3:");
scanf("%d",&i3);
bal=fees-(i1+i2+i3);
printf("\n enter the instalment4:");
scanf("%d",&i4);
bal=fees-(i1+i2+i3+i4);
printf("\n enter the instalment5:");
scanf("%d",&i5);
bal=fees-(i1+i2+i3+i4+i5);
printf("\n enter the instalment6:");
scanf("%d",&i6);
bal=fees-(i1+i2+i3+i4+i5+i6);
printf("\n balance %d",bal);
}
