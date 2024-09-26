// Sample Java program for testing with nested structures
public class TestJavaProgram {

    // Correct method
    public static void main(String[] args) {
        int x = 10;

        // Decision structure without curly braces
        if (x > 5)
            System.out.println("x is greater than 5");

        // Nested if-else without curly braces
        if (x > 5)
            if (x < 20)
                System.out.println("x is between 5 and 20");
            else
                System.out.println("x is 20 or more");
        else
            System.out.println("x is 5 or less");

        // Decision structure with else-if without curly braces
        if (x > 5)
            System.out.println("x is greater than 5");
        else if (x == 5)
            System.out.println("x is equal to 5");
        else
            System.out.println("x is less than 5");

        // Nested switch statement without curly braces in cases
        switch (x) {
            case 1:
                System.out.println("x is 1");
                switch (x + 1) {
                    case 2:
                        System.out.println("Nested case: x + 1 is 2");
                        break;
                }
                break;
            case 10:
                System.out.println("x is 10");
                break;
            default:
                System.out.println("x is neither 1 nor 10");
        }

        // While loop without curly braces
        while (x > 0)
            x--;

        // Nested while loop without curly braces
        while (x > -5)
            while (x > -10)
                x--;

        // For loop without curly braces
        for (int i = 0; i < 5; i++)
            System.out.println(i);

        // Nested for loop without curly braces
        for (int i = 0; i < 5; i++)
            for (int j = 0; j < 3; j++)
                System.out.println(i + "," + j);

        // Do-while loop without curly braces
        do
            x--;
        while (x > 0);

        // Nested do-while loop without curly braces
        do
            do
                x--;
            while (x > -5);
        while (x > -10);
    }

    // Incorrect method without body
    public void incorrectMethod() 

    // Another correct method
    public void anotherMethod() {
        System.out.println("This is another method.");
    }

    // Method with single statement without braces
    public void singleStatementMethod()
        System.out.println("Single statement without braces");

    // Nested decision structure in a method
    public void nestedDecisionMethod() {
        int a = 5;
        if (a > 0)
            if (a < 10)
                System.out.println("a is between 0 and 10");
    }

    // Nested loop in a method
    public void nestedLoopMethod() {
        for (int i = 0; i < 3; i++)
            while (i < 2)
                System.out.println("Nested loop");
    }
}
