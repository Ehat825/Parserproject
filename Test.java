public class Test {
    public static void main(String[] args) {
        int x = 10;
        if (x > 5)
            System.out.println("x is greater than 5");
        else
            System.out.println("x is not greater than 5");

        for (int i = 0; i < 5; i++)
            System.out.println(i);

        while (x > 0)
            x--;

        do
            x++;
        while (x < 5);
    }

    public void exampleMethod() {
        System.out.println("This is an example method.");
    }
}
