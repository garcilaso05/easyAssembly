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
@ test1.c:2:     int A = 2;
	mov	r3, #2	@ tmp118,
	str	r3, [fp, #-8]	@ tmp118, A
@ test1.c:3:     int suma = 5 + A;
	ldr	r3, [fp, #-8]	@ tmp120, A
	add	r3, r3, #5	@ suma_4, tmp120,
	str	r3, [fp, #-12]	@ suma_4, suma
@ test1.c:4:     int resta = 6 - A;
	ldr	r3, [fp, #-8]	@ tmp122, A
	rsb	r3, r3, #6	@ resta_5, tmp122,
	str	r3, [fp, #-16]	@ resta_5, resta
@ test1.c:5:     int multiplicacion = 7 * A;
	ldr	r2, [fp, #-8]	@ tmp123, A
	mov	r3, r2	@ tmp124, tmp123
	lsl	r3, r3, #3	@ tmp124, tmp124,
	sub	r3, r3, r2	@ multiplicacion_6, tmp124, tmp123
	str	r3, [fp, #-20]	@ multiplicacion_6, multiplicacion
@ test1.c:6:     int division = 4 / A;
	ldr	r1, [fp, #-8]	@, A
	mov	r0, #4	@,
	bl	__aeabi_idiv		@
	mov	r3, r0	@ division_7,
	str	r3, [fp, #-24]	@ division_7, division
@ test1.c:7:     int modulo = 4 % A;
	mov	r3, #4	@ tmp131,
	ldr	r1, [fp, #-8]	@, A
	mov	r0, r3	@, tmp131
	bl	__aeabi_idivmod		@
	mov	r3, r1	@ modulo_8,
	str	r3, [fp, #-28]	@ modulo_8, modulo
@ test1.c:9:     int resultado = (suma + resta) * (multiplicacion - division);
	ldr	r2, [fp, #-12]	@ tmp141, suma
	ldr	r3, [fp, #-16]	@ tmp142, resta
	add	r3, r2, r3	@ _1, tmp141, tmp142
@ test1.c:9:     int resultado = (suma + resta) * (multiplicacion - division);
	ldr	r1, [fp, #-20]	@ tmp143, multiplicacion
	ldr	r2, [fp, #-24]	@ tmp144, division
	sub	r2, r1, r2	@ _2, tmp143, tmp144
@ test1.c:9:     int resultado = (suma + resta) * (multiplicacion - division);
	mul	r3, r2, r3	@ resultado_9, _2, resultado_9
	str	r3, [fp, #-32]	@ resultado_9, resultado
@ test1.c:11:     return 0;
	mov	r3, #0	@ _10,
@ test1.c:12: }
	mov	r0, r3	@, <retval>
	sub	sp, fp, #4	@,,
	@ sp needed	@
	pop	{fp, lr}	@
	bx	lr	@
	.size	main, .-main
	.global	__aeabi_idivmod
	.global	__aeabi_idiv
	.ident	"GCC: (Arch Repository) 14.2.0"
