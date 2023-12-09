# Simplic Syntax
When parsing, the compiler will isolate only the code cells. Can include code cells, but the order of execution does not matter; all codes will still have one entry point at function main.
```
func main () {
    let x = 3, y = 2
    print(f"the sum of numbers = {x + y}")
}
```
## Objective
This file is to demonstrate how the syntax of simplic should look like. Specifically, I'm conflicted with the `: type` similar to typescript, golang, or some other newer languages. This should make the code much easier to parse. Simplic is statically typed, but also use implicit typing in many cases. Regardless, the syntax for type specification has to be consistent for variables, arguments, and function return types. 
```
func helperFunctions : float (meshPoints : array<int>) {
    let sum = 0
    for i in meshPoints {
        # can optionally specify type explicitly
        let v : float = fixResult(i)
        sum += v / meshPoints.length
    }
    return sum
}
```

## Generic Structs and Functions
```
struct Entity<T> {
    let x : T
    let y : int
}

func CollectEntity<T> : Array<Entity<T>> (arr : Array<T>) {
    let l = Array<Entity<T>>{ size: arr.length }
    for i, a in enumerate(arr) {
        l[i] = Entity<T>{ x = a, y = i }
    }
    return l
}

```