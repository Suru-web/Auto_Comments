
// Counts the number of digits in an integer.
int countDigits(int num) { int count = 0; while (num) { num /= 10; count++; } return count; }