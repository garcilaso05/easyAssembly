	.cpu arm7tdmi
	.arch armv4t
	.fpu softvfp
	.eabi_attribute 20, 1	@ Tag_ABI_FP_denormal
	.eabi_attribute 21, 1	@ Tag_ABI_FP_exceptions
	.eabi_attribute 23, 3	@ Tag_ABI_FP_number_model
	.eabi_attribute 24, 1	@ Tag_ABI_align8_needed
	.eabi_attribute 25, 1	@ Tag_ABI_align8_preserved
	.eabi_attribute 26, 1	@ Tag_ABI_enum_size
	.eabi_attribute 30, 6	@ Tag_ABI_optimization_goals
	.eabi_attribute 34, 0	@ Tag_CPU_unaligned_access
	.eabi_attribute 18, 4	@ Tag_ABI_PCS_wchar_t
	.file	"test1.c"
@ GNU C17 (Arch Repository) version 14.2.0 (arm-none-eabi)
@	compiled by GNU C version 14.2.1 20240910, GMP version 6.3.0, MPFR version 4.2.1, MPC version 1.3.1, isl version isl-0.27-GMP

@ GGC heuristics: --param ggc-min-expand=100 --param ggc-min-heapsize=131072
@ options passed: -mcpu=arm7tdmi -mthumb-interwork -mfloat-abi=soft -marm -march=armv4t -O0
	.text
	.global	A
	.data
	.align	2
	.type	A, %object
	.size	A, 4
A:
	.word	2
	.text
	.align	2
	.global	main
	.syntax unified
	.arm
	.type	main, %function
main:
	@ Function supports interworking.
	@ args = 0, pretend = 0, frame = 24
	@ frame_needed = 1, uses_anonymous_args = 0
	push	{fp, lr}	@
	add	fp, sp, #4	@,,
	sub	sp, sp, #24	@,,
@ test1.c:4:     int suma = 5 + A;
	ldr	r3, .L3	@ tmp123,
	ldr	r3, [r3]	@ A.0_1, A
@ test1.c:4:     int suma = 5 + A;
	add	r3, r3, #5	@ suma_9, A.0_1,
	str	r3, [fp, #-8]	@ suma_9, suma
@ test1.c:5:     int resta = 6 - A;
	ldr	r3, .L3	@ tmp125,
	ldr	r3, [r3]	@ A.1_2, A
@ test1.c:5:     int resta = 6 - A;
	rsb	r3, r3, #6	@ resta_10, A.1_2,
	str	r3, [fp, #-12]	@ resta_10, resta
@ test1.c:6:     int multiplicacion = 7 * A;
	ldr	r3, .L3	@ tmp127,
	ldr	r2, [r3]	@ A.2_3, A
@ test1.c:6:     int multiplicacion = 7 * A;
	mov	r3, r2	@ tmp128, A.2_3
	lsl	r3, r3, #3	@ tmp128, tmp128,
	sub	r3, r3, r2	@ multiplicacion_11, tmp128, A.2_3
	str	r3, [fp, #-16]	@ multiplicacion_11, multiplicacion
@ test1.c:7:     int division = 4 / A;
	ldr	r3, .L3	@ tmp130,
	ldr	r3, [r3]	@ A.3_4, A
@ test1.c:7:     int division = 4 / A;
	mov	r1, r3	@, A.3_4
	mov	r0, #4	@,
	bl	__aeabi_idiv		@
	mov	r3, r0	@ division_12,
	str	r3, [fp, #-20]	@ division_12, division
@ test1.c:8:     int modulo = 4 % A;
	ldr	r3, .L3	@ tmp134,
	ldr	r3, [r3]	@ A.4_5, A
@ test1.c:8:     int modulo = 4 % A;
	mov	r2, #4	@ tmp135,
	mov	r1, r3	@, A.4_5
	mov	r0, r2	@, tmp135
	bl	__aeabi_idivmod		@
	mov	r3, r1	@ modulo_13,
	str	r3, [fp, #-24]	@ modulo_13, modulo
@ test1.c:10:     int resultado = (suma + resta) * (multiplicacion - division);
	ldr	r2, [fp, #-8]	@ tmp145, suma
	ldr	r3, [fp, #-12]	@ tmp146, resta
	add	r3, r2, r3	@ _6, tmp145, tmp146
@ test1.c:10:     int resultado = (suma + resta) * (multiplicacion - division);
	ldr	r1, [fp, #-16]	@ tmp147, multiplicacion
	ldr	r2, [fp, #-20]	@ tmp148, division
	sub	r2, r1, r2	@ _7, tmp147, tmp148
@ test1.c:10:     int resultado = (suma + resta) * (multiplicacion - division);
	mul	r3, r2, r3	@ resultado_14, _7, resultado_14
	str	r3, [fp, #-28]	@ resultado_14, resultado
@ test1.c:12:     return 0;
	mov	r3, #0	@ _15,
@ test1.c:13: }
	mov	r0, r3	@, <retval>
	sub	sp, fp, #4	@,,
	@ sp needed	@
	pop	{fp, lr}	@
	bx	lr	@
.L4:
	.align	2
.L3:
	.word	A
	.size	main, .-main
	.global	__aeabi_idivmod
	.global	__aeabi_idiv
	.ident	"GCC: (Arch Repository) 14.2.0"
