#include <stdio.h>

#define MAX_NAME_LENGTH 50
#define MAX_BUFFER_SIZE 100
#define MAX_CUSTUMER 3

typedef struct { // define structure for date
    int day, month, year;
} date;

typedef struct { // define structure for CustomerInfo info
    char name[MAX_NAME_LENGTH];
    int accountNumber;
    double balance;
    date lastTrans;
} CustomerInfo;

// Function prototypes
void getCustomerName(CustomerInfo *CustomerInfoPointer);

void getAccountNumber(CustomerInfo *CustomerInfoPointer);

void getLastTransDate(CustomerInfo *CustomerInfoPointer);

void getBalance(CustomerInfo *CustomerInfoPointer);

void printCustomerInfo(CustomerInfo *CustomerInfoPointer);

int isValidDate(int day, int month, int year);

void clearInputBuffer();

void getCustomerInfo(CustomerInfo *CustomerInfoPointer);

int main() {
    int i;
    CustomerInfo CustomerInfos[MAX_CUSTUMER];

    for (i = 0; i < MAX_CUSTUMER; i++) { // for loop so the functions work 3 times before printing the output
        getCustomerInfo(&CustomerInfos[i]);
    }

    printf("\n\n%25s\t%13s\t%12s\t%s\n\n", "Name", "Account Number", "Balance", "Date of Last Transaction");

    for (i = 0; i < MAX_CUSTUMER; i++) {
        printCustomerInfo(&CustomerInfos[i]);
    }

    return 0;
}

// Function to get CustomerInfo's name
void getCustomerName(CustomerInfo *CustomerInfoPointer) {
    printf("Enter CustomerInfo's name: ");
    fgets(CustomerInfoPointer->name, 50, stdin); // fgets to scan the name in
}

void getAccountNumber(CustomerInfo *CustomerInfoPointer) {
    printf("Enter account number: ");
    if (scanf("%d", &CustomerInfoPointer->accountNumber) != 1) {
        printf("Invalid input for account number. Please enter a valid integer.\n");
        clearInputBuffer();
        while (getchar() != '\n');                                  // Clear input buffer
        getAccountNumber(CustomerInfoPointer); // Recursive call to try again
    }
}

void getLastTransDate(CustomerInfo *CustomerInfoPointer) {
    printf("Enter date of last transaction (DD MM YYYY): ");
    if (scanf("%d %d %d", &CustomerInfoPointer->lastTrans.day, &CustomerInfoPointer->lastTrans.month,
              &CustomerInfoPointer->lastTrans.year) != 3 ||
        !isValidDate(CustomerInfoPointer->lastTrans.day, CustomerInfoPointer->lastTrans.month,
                     CustomerInfoPointer->lastTrans.year)) {
        printf("Invalid input for date. Please enter a valid date (DD MM YYYY).\n");
        clearInputBuffer();
        while (getchar() != '\n'); // Clear input buffer
        getLastTransDate(CustomerInfoPointer); // Recursive call to try again
    }
}

void getBalance(CustomerInfo *CustomerInfoPointer) {
    printf("Enter balance: ");
    if (scanf("%lf", &CustomerInfoPointer->balance) != 1) {
        printf("Invalid input for balance. Please enter a valid numerical value.\n");
        clearInputBuffer();
        while (getchar() != '\n');                            // Clear input buffer
        getBalance(CustomerInfoPointer); // Recursive call to try again
    }
}

// Function to print CustomerInfo details
void printCustomerInfo(CustomerInfo *CustomerInfoPointer) {
    printf("%-25s\t%13d\t%12.2lf\t%d-%d-%d\n", CustomerInfoPointer->name, CustomerInfoPointer->accountNumber,
           CustomerInfoPointer->balance, CustomerInfoPointer->lastTrans.day, CustomerInfoPointer->lastTrans.month,
           CustomerInfoPointer->lastTrans.year);
}

int isValidDate(int day, int month, int year) {
    // Basic validation for the month and day range
    if (month < 1 || month > 12 || day < 1 || day > 31)
        return 0;

    // Additional validation for specific months
    if (month == 4 || month == 6 || month == 9 || month == 11) {
        return day <= 30;
    } else if (month == 2) {
        // Leap year check
        if ((year % 4 == 0 && year % 100 != 0) || (year % 400 == 0))
            return day <= 29;
        else
            return day <= 28;
    }

    return 1;
}

void clearInputBuffer() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

void getCustomerInfo(CustomerInfo *CustomerInfoPointer) {
    getCustomerName(CustomerInfoPointer);
    getAccountNumber(CustomerInfoPointer);
    getLastTransDate(CustomerInfoPointer);
    getBalance(CustomerInfoPointer);
    clearInputBuffer();
    printf("\n");
}