#Calculator program with help from ChatGPT 

options = ["Addition", "Subtraction", "Multiplication", "Division", "Modulus", "Floor Division", "Exponentiation", "Quit"]
print("Welcome to the Calculator Program. Please select an option from the list below.")
for i, option in enumerate(options):
    print(f"{i+1}. {option}")

while True:
    choice = int(input("Enter your choice: "))

    if choice == 1:
        numbers = [float(input(f"Enter number {i+1}: ")) for i in range(2)]
        result = sum(numbers)
        print("The sum is", result)
    elif choice == 2:
        number = [float(input(f"Enter number {i+1}: ")) for i in range(2)]
        result = number[0] - number[1]
        print("The difference is", result)
    elif choice == 3:
        numbers = [float(input(f"Enter number {i+1}: ")) for i in range(2)]
        result = numbers[0] * numbers[1]
        print("The product is", result)
    elif choice == 4:
        numbers = [float(input(f"Enter number {i+1}: ")) for i in range(2)]
        if numbers[1] == 0:
            print("You cannot divide by zero")
        else:
            result = numbers[0] / numbers[1]
            print("The quotient is", result)
    elif choice == 5:
        number = [int(float(input(f"Enter number {i+1}: ")) for i in range(2))]
        result = number[0] % number[1]
        print("The remainder is", result)
    elif choice == 6:
        number  = [float(input(f"Enter number {i+1}: ")) for i in range(2)]
        result = number[0] // number[1]
        print("The floor division is", result)
    elif choice == 7:
        number = [float(input(f"Enter number {i+1}: ")) for i in range(2)]
        result = number[0] ** number[1]
        print("The exponentiation is", result)
    else:
        choice == 8
        print("Thank you for using the calculator program")
        break

    


    







#