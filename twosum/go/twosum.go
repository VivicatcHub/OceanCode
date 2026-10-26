// Two Sum : trouver deux indices i < j tels que nums[i] + nums[j] == target.
package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
)

const usage = "usage: twosum <target>   (nombres lus sur stdin)"
const limit = 1_000_000_000_000_000_000

// twoSum renvoie (i, j, true) avec i < j et nums[i]+nums[j] == target,
// ou (0, 0, false) s'il n'y a pas de solution.
// S'il y a plusieurs solutions : le plus petit j, puis le plus petit i.
// Doit être en O(n).
func twoSum(nums []int64, target int64) (int, int, bool) {
	seen := make(map[int64]int64)
	for index, value := range nums {
		complement := target - value
		val, ok := seen[complement]
		if ok {
			return int(val) , index, true
		} else {
			_, ok := seen[value]
			if !ok {
				seen[value] = int64(index)
			}
		}
	}
	return 0, 0, false
}

func die(msg string) {
	fmt.Fprintf(os.Stderr, "error: %s\n%s\n", msg, usage)
	os.Exit(1)
}

func parseInt(s string) int64 {
	digits := s
	if len(digits) > 0 && digits[0] == '-' {
		digits = digits[1:]
	}
	if digits == "" {
		die(fmt.Sprintf("invalid number '%s'", s))
	}
	for _, c := range []byte(digits) {
		if c < '0' || c > '9' {
			die(fmt.Sprintf("invalid number '%s'", s))
		}
	}
	n, err := strconv.ParseInt(s, 10, 64)
	if err != nil || n > limit || n < -limit {
		die(fmt.Sprintf("number out of range '%s'", s))
	}
	return n
}

func main() {
	if len(os.Args) != 2 {
		die("wrong number of arguments")
	}
	target := parseInt(os.Args[1])

	var nums []int64
	sc := bufio.NewScanner(bufio.NewReader(os.Stdin))
	sc.Buffer(make([]byte, 1<<20), 1<<20)
	sc.Split(bufio.ScanWords)
	for sc.Scan() {
		nums = append(nums, parseInt(sc.Text()))
	}
	if err := sc.Err(); err != nil {
		die(err.Error())
	}

	if i, j, ok := twoSum(nums, target); ok {
		fmt.Printf("%d %d\n", i, j)
	} else {
		fmt.Println("none")
	}
}
