public class testing{
    // Calculates the greatest common divisor using recursion
int gcd(int a, int b) { while (b != 0) { int temp = b; b = a % b; a = temp; } return a; }
}