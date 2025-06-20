	.file	"test1.c"
	.intel_syntax noprefix
# GNU C17 (GCC) version 14.2.1 20250207 (x86_64-pc-linux-gnu)
#	compiled by GNU C version 14.2.1 20250207, GMP version 6.3.0, MPFR version 4.2.1, MPC version 1.3.1, isl version isl-0.27-GMP

# GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
# options passed: -masm=intel -mtune=generic -march=x86-64 -O0
	.text
	.globl	sumar
	.type	sumar, @function
sumar:
.LFB0:
	.cfi_startproc
	push	rbp	#
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp	#,
	.cfi_def_cfa_register 6
	mov	DWORD PTR -20[rbp], edi	# a, a
	mov	DWORD PTR -24[rbp], esi	# b, b
# test1.c:3:     int r = a + b;
	mov	edx, DWORD PTR -20[rbp]	# tmp104, a
	mov	eax, DWORD PTR -24[rbp]	# tmp105, b
	add	eax, edx	# r_3, tmp104
	mov	DWORD PTR -4[rbp], eax	# r, r_3
# test1.c:4:     return r;
	mov	eax, DWORD PTR -4[rbp]	# _4, r
# test1.c:6: }
	pop	rbp	#
	.cfi_def_cfa 7, 8
	ret	
	.cfi_endproc
.LFE0:
	.size	sumar, .-sumar
	.globl	main
	.type	main, @function
main:
.LFB1:
	.cfi_startproc
	push	rbp	#
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	mov	rbp, rsp	#,
	.cfi_def_cfa_register 6
	sub	rsp, 32	#,
# test1.c:9:     int A = 2;
	mov	DWORD PTR -28[rbp], 2	# A,
# test1.c:10:     int suma = sumar(5, A);
	mov	eax, DWORD PTR -28[rbp]	# tmp102, A
	mov	esi, eax	#, tmp102
	mov	edi, 5	#,
	call	sumar	#
	mov	DWORD PTR -24[rbp], eax	# suma, tmp103
# test1.c:11:     int resta = 6 - A;
	mov	eax, 6	# tmp107,
	sub	eax, DWORD PTR -28[rbp]	# resta_7, A
	mov	DWORD PTR -20[rbp], eax	# resta, resta_7
# test1.c:12:     int multiplicacion = 7 * A;
	mov	edx, DWORD PTR -28[rbp]	# tmp108, A
	mov	eax, edx	# tmp109, tmp108
	sal	eax, 3	# tmp110,
	sub	eax, edx	# tmp111, tmp108
	mov	DWORD PTR -16[rbp], eax	# multiplicacion, tmp111
# test1.c:13:     int division = 4 / A;
	mov	eax, 4	# tmp115,
	cdq
	idiv	DWORD PTR -28[rbp]	# A
	mov	DWORD PTR -12[rbp], eax	# division, division_9
# test1.c:14:     int modulo = 4 % A;
	mov	eax, 4	# tmp117,
	cdq
	idiv	DWORD PTR -28[rbp]	# A
	mov	DWORD PTR -8[rbp], edx	# modulo, modulo_10
# test1.c:16:     int resultado = (suma + resta) * (multiplicacion - division);
	mov	edx, DWORD PTR -24[rbp]	# tmp120, suma
	mov	eax, DWORD PTR -20[rbp]	# tmp121, resta
	add	edx, eax	# _1, tmp121
# test1.c:16:     int resultado = (suma + resta) * (multiplicacion - division);
	mov	eax, DWORD PTR -16[rbp]	# tmp122, multiplicacion
	sub	eax, DWORD PTR -12[rbp]	# _2, division
# test1.c:16:     int resultado = (suma + resta) * (multiplicacion - division);
	imul	eax, edx	# resultado_11, _1
	mov	DWORD PTR -4[rbp], eax	# resultado, resultado_11
# test1.c:18:     return 0;
	mov	eax, 0	# _12,
# test1.c:19: }
	leave	
	.cfi_def_cfa 7, 8
	ret	
	.cfi_endproc
.LFE1:
	.size	main, .-main
	.ident	"GCC: (GNU) 14.2.1 20250207"
	.section	.note.GNU-stack,"",@progbits
