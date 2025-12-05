# ARM

ARM 在其架构中不断引入硬件安全特性，以应对日益复杂的软件漏洞和安全威胁，特别是内存安全漏洞（如缓冲区溢出和释放后使用）。本节主要讲解 ARM 中的硬件安全设计原理：

- [ARM PAC](pac.html)：主要针对控制流完整性 (Control-Flow Integrity, CFI) 漏洞，例如返回导向编程 (ROP) 和跳转导向编程 (JOP) 攻击。这些攻击通过篡改栈上的返回地址或函数指针来劫持程序的执行流程。
- [ARM MTE](mte.html)：主要针对内存安全违规 (Memory Safety Violations)，包括空间安全 (Spatial Safety)（如缓冲区溢出）和时间安全 (Temporal Safety)（如释放后使用 Use-After-Free）。
