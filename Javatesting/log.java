package Javatesting;

import java.util.Scanner;

public class log {
    public static void main(String[] args) {
        Scanner  keyboard = new Scanner(System.in);
        System.out.println("What is your name?");

        String name = keyboard.nextLine();

        if (name.equals(anObject: "Tom")) {
            System.out.println("Hello Tom! Welcome back!");
        } else {
            System.out.println("Hello " + name + "! You are not Tom!");
            
        }

        
    }
}