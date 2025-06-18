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
	@ args = 0, pretend = 0, frame = 24
	@ frame_needed = 1, uses_anonymous_args = 0
	@ link register save eliminated.
	str	fp, [sp, #-4]!	@,
	add	fp, sp, #0	@,,
	sub	sp, sp, #28	@,,
@ test1.c:4:     int suma = 5 + A;
	mov	r3, #7	@ tmp118,
	str	r3, [fp, #-8]	@ tmp118, suma
@ test1.c:5:     int resta = 6 - A;
	mov	r3, #4	@ tmp119,
	str	r3, [fp, #-12]	@ tmp119, resta
@ test1.c:6:     int multiplicacion = 7 * A;
	mov	r3, #14	@ tmp120,
	str	r3, [fp, #-16]	@ tmp120, multiplicacion
@ test1.c:7:     int division = 4 / A;
	mov	r3, #2	@ tmp121,
	str	r3, [fp, #-20]	@ tmp121, division
@ test1.c:8:     int modulo = 4 % A;
	mov	r3, #0	@ tmp122,
	str	r3, [fp, #-24]	@ tmp122, modulo
@ test1.c:10:     int resultado = (suma + resta) * (multiplicacion - division);
	ldr	r2, [fp, #-8]	@ tmp123, suma
	ldr	r3, [fp, #-12]	@ tmp124, resta
	add	r3, r2, r3	@ _1, tmp123, tmp124
@ test1.c:10:     int resultado = (suma + resta) * (multiplicacion - division);
	ldr	r1, [fp, #-16]	@ tmp125, multiplicacion
	ldr	r2, [fp, #-20]	@ tmp126, division
	sub	r2, r1, r2	@ _2, tmp125, tmp126
@ test1.c:10:     int resultado = (suma + resta) * (multiplicacion - division);
	mul	r3, r2, r3	@ resultado_8, _2, resultado_8
	str	r3, [fp, #-28]	@ resultado_8, resultado
@ test1.c:12:     return 0;
	mov	r3, #0	@ _9,
@ test1.c:13: }
	mov	r0, r3	@, <retval>
	add	sp, fp, #0	@,,
	@ sp needed	@
	ldr	fp, [sp], #4	@,
	bx	lr	@
	.size	main, .-main
	.ident	"GCC: (Arch Repository) 14.2.0"
