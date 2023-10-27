class Main {
    public static int foo(int x) {
        return x * 10 + 42; 
    }

    public static int bar(int n) {
        int r = 1;
        while (n > 1){
            r = n * r;
            n -= 1;
        }
        return r;
    }

    public static void main(String[] args) {
        System.out.println(foo(5));
    }
}

