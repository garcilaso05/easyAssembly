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
	.align	2
	.global	sumar
	.syntax unified
	.arm
	.type	sumar, %function
sumar:
	@ Function supports interworking.
	@ args = 0, pretend = 0, frame = 16
	@ frame_needed = 1, uses_anonymous_args = 0
	@ link register save eliminated.
	str	fp, [sp, #-4]!	@,
	add	fp, sp, #0	@,,
	sub	sp, sp, #20	@,,
	str	r0, [fp, #-16]	@ a, a
	str	r1, [fp, #-20]	@ b, b
@ test1.c:3:     int r = a + b;
	ldr	r2, [fp, #-16]	@ tmp117, a
	ldr	r3, [fp, #-20]	@ tmp118, b
	add	r3, r2, r3	@ r_3, tmp117, tmp118
	str	r3, [fp, #-8]	@ r_3, r
@ test1.c:4:     return r;
	ldr	r3, [fp, #-8]	@ _4, r
@ test1.c:6: }
	mov	r0, r3	@, <retval>
	add	sp, fp, #0	@,,
	@ sp needed	@
	ldr	fp, [sp], #4	@,
	bx	lr	@
	.size	sumar, .-sumar
	.align	2
	.global	main
	.syntax unified
	.arm
	.type	main, %function
main:
	@ Function supports interworking.
	@ args = 0, pretend = 0, frame = 32
	@ frame_needed = 1, uses_anonymous_args = 0
	push	{fp, lr}	@
	add	fp, sp, #4	@,,
	sub	sp, sp, #32	@,,
@ test1.c:9:     int A = 2;
	mov	r3, #2	@ tmp118,
	str	r3, [fp, #-8]	@ tmp118, A
@ test1.c:10:     int suma = sumar(5, A);
	ldr	r1, [fp, #-8]	@, A
	mov	r0, #5	@,
	bl	sumar		@
	str	r0, [fp, #-12]	@, suma
@ test1.c:11:     int resta = 6 - A;
	ldr	r3, [fp, #-8]	@ tmp120, A
	rsb	r3, r3, #6	@ resta_7, tmp120,
	str	r3, [fp, #-16]	@ resta_7, resta
@ test1.c:12:     int multiplicacion = 7 * A;
	ldr	r2, [fp, #-8]	@ tmp121, A
	mov	r3, r2	@ tmp122, tmp121
	lsl	r3, r3, #3	@ tmp122, tmp122,
	sub	r3, r3, r2	@ multiplicacion_8, tmp122, tmp121
	str	r3, [fp, #-20]	@ multiplicacion_8, multiplicacion
@ test1.c:13:     int division = 4 / A;
	ldr	r1, [fp, #-8]	@, A
	mov	r0, #4	@,
	bl	__aeabi_idiv		@
	mov	r3, r0	@ division_9,
	str	r3, [fp, #-24]	@ division_9, division
@ test1.c:14:     int modulo = 4 % A;
	mov	r3, #4	@ tmp129,
	ldr	r1, [fp, #-8]	@, A
	mov	r0, r3	@, tmp129
	bl	__aeabi_idivmod		@
	mov	r3, r1	@ modulo_10,
	str	r3, [fp, #-28]	@ modulo_10, modulo
@ test1.c:16:     int resultado = (suma + resta) * (multiplicacion - division);
	ldr	r2, [fp, #-12]	@ tmp139, suma
	ldr	r3, [fp, #-16]	@ tmp140, resta
	add	r3, r2, r3	@ _1, tmp139, tmp140
@ test1.c:16:     int resultado = (suma + resta) * (multiplicacion - division);
	ldr	r1, [fp, #-20]	@ tmp141, multiplicacion
	ldr	r2, [fp, #-24]	@ tmp142, division
	sub	r2, r1, r2	@ _2, tmp141, tmp142
@ test1.c:16:     int resultado = (suma + resta) * (multiplicacion - division);
	mul	r3, r2, r3	@ resultado_11, _2, resultado_11
	str	r3, [fp, #-32]	@ resultado_11, resultado
@ test1.c:18:     return 0;
	mov	r3, #0	@ _12,
@ test1.c:19: }
	mov	r0, r3	@, <retval>
	sub	sp, fp, #4	@,,
	@ sp needed	@
	pop	{fp, lr}	@
	bx	lr	@
	.size	main, .-main
	.global	__aeabi_idivmod
	.global	__aeabi_idiv
	.ident	"GCC: (Arch Repository) 14.2.0"
