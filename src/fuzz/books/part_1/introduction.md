# Introduction to Software Testing

在进入本书的核心内容之前，让我们先介绍软件测试的基本概念。为什么要测试软件？如何测试软件？如何判断一个测试是否成功？如何知道是否已经测试足够？在本章中，让我们回顾最重要的概念，同时熟悉 Python 和交互式笔记本。

本章（以及本书）并非旨在取代一本测试教科书；请参阅文末的[背景](#backgroud)部分，了解推荐的阅读材料。

## Simple Testing

让我们从一个简单的例子开始。您的同事被要求实现一个平方根函数 \\( \sqrt{x} \\) 。（我们暂且假设当前环境中还没有这个函数。）在研究完[Newton-Raphson](https://en.wikipedia.org/wiki/Newton%27s_method)方法后，她提出了下面的 Python 代码，并声称这个 `my_sqrt()` 函数确实可以计算平方根。

``` rust
fn my_sqrt(x: f64) -> f64 {
    /// Computes the square root of x, using the Newton-Raphson method
    let mut approx = x / 2.0;
    let mut guess = (approx + x / approx) / 2.0;
    
    while approx != guess {
        approx = guess;
        guess = (approx + x / approx) / 2.0;
    }
    
    approx
}
```

您现在的任务是去验证这个函数是否真的能做到它声称的功能。

### Understanding Python Programs

此处不再对 `Python` 的概念进行介绍。

在本项目中，部分简单代码会通过 `Rust` 进行重写，这样就能够使得读者在阅读时直接在网页中运行代码，而不需要自行搭建环境。例如：

``` rust
{{#include ../codes/my_sqrt.rs:0:11}}

println!("{}", my_sqrt(4.0));
```

## Automating Test Execution

到目前为止，我们一直采用手动方式测试上述程序，即手动运行并人工检查结果。这是一种非常灵活的测试方法，但从长远来看，效率相当低下：

1. 手动检查的执行次数及其结果非常有限
2. 程序有任何更改后，都必须重复测试过程

这就是为什么自动化测试非常有用。一种简单的方法是让计算机先进行计算，然后再检查结果。

例如，这段代码会自动测试 \\( \sqrt{4} = 2 \\) 是否成立：

``` rust
{{#include ../codes/my_sqrt.rs:0:11}}


let result = my_sqrt(4.0);
let expected_result = 2.0;
if result == expected_result {
    println!("Test passed")
} else {
    println!("Test failed")
}
```

这个测试的好处在于我们可以反复运行它，从而确保至少能正确计算出 4 的平方根。不过，仍然存在一些问题：

1. 我们需要五行代码来编写一个测试
2. 我们不在乎四舍五入误差
3. 我们只检查一个输入（以及一个结果）

让我们逐一解决这些问题。首先，让我们让测试更紧凑一些。几乎所有编程语言都有一种自动检查条件是否成立并在不成立时停止执行的方法。这被称为断言，对于测试非常有用。

在 Python 中， `assert` 语句接受一个条件，如果条件为真，则什么都不会发生。（如果一切按预期工作，你就不应该感到困扰。）然而，如果条件评估为假， `assert` 会引发一个异常，表示一个测试刚刚失败。

``` rust
{{#include ../codes/my_sqrt.rs:0:11}}

assert!(my_sqrt(4.0) == 2.0);
```

## The Limits of Testing

在原书中做了多种测试对上面的 `my_sqrt` 函数进行了验证。**请记住，尽管我们竭尽全力进行测试，但您始终只是在针对一组有限的输入来检验功能。因此，总可能存在未经测试的输入，导致函数在这些情况下仍可能出错**。

例如，如果此时这个程序计算 \\( \sqrt{0} \\)，就会导致除零错误。

``` py
my_sqrt(0)
```

在我们目前的测试中，并未验证这种情况（即 \\( \sqrt{0} = 0 \\) 的条件）。这意味着，一个基于 \\( \sqrt{0} = 0 \\) 这一前提的程序会意外地失败。但即使我们将随机生成器的输入范围设置为 0 到 1000000（而非 1 到 1000000），它恰好生成零值的概率仍是百万分之一。如果一个函数在少数特定值上的行为截然不同，简单的随机测试很难覆盖到这些情况。

**因此，我们必须记住，尽管广泛的测试可以让我们对程序的正确性有高度的信心，但它并不能保证程序在所有的未来执行中都是正确的。即使是运行时验证（它会检查每一个结果），也只能保证如果它产生了一个结果，那么这个结果将是正确的；但并不能保证未来的执行不会导致检查失败**。

这正是我们在本课程后续内容中要做的事情：设计能帮助我们彻底测试程序的技术，以及帮助我们检查其状态正确性的方法。祝您学习愉快！

## Backgroud

- An all-new modern, comprehensive, and online textbook on testing is ["Effective Software Testing: A Developer's Guide" [Maurício Aniche, 2022]](https://www.effective-software-testing.com/)
- For this book, we are also happy to recommend ["Software Testing and Analysis"[Pezzè et al, 2008]](http://ix.cs.uoregon.edu/~michal/book/)
- Other important must-reads with a comprehensive approach to software testing, including psychology and organization, include ["The Art of Software Testing"[Myers et al, 2004]](https://dl.acm.org/citation.cfm?id=983238) as well as ["Software Testing Techniques" [Beizer et al, 1990]](https://dl.acm.org/citation.cfm?id=79060).

## Exercise

### Testing Shellsort

考虑以下 `shellsort` 函数的实现，它接受一个元素列表并 (推测性地) 对其进行排序：

``` rust
{{#include ../codes/shellsort.rs}}
```

你的任务是使用各种输入彻底测试 `shellsort()`：

- 手动测试用例
- 随机输入
