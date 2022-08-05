TITLE Data Validation, Looping, Constants     (Proj3_sekujk.asm)

; Author: Kevin Sekuj
; Last Modified: 2/7/2021
; OSU email address: sekujk@oregonstate.edu
; Course number/section:   CS271 Section 400_W2021
; Project Number: 3                Due Date: 2/7/2021

; Description: Program which asks a user to input numbers within two ranges of 
; four negative numbers. These negative number ranges are defined as constants.
; When the user has entered a series of valid negative numbers, they may enter
; any positive number (including zero) to calculate and display the numbers' 
; count, sum, maximum, minimum, rounded average, and average as a decimal rounded to
; the hundredths place. The user may also exit the program without inputting any
; valid numbers, if they wish. 

INCLUDE Irvine32.inc

LIMIT_LOWER		=  -200		; limit constants, allowing input in [-200, -100] or [-50, -1] 
LIMIT_LOWERMID	=  -100		; inclusive
LIMIT_UPPERMID	=  -50
LIMIT_UPPER		=  -1		

.data

; greeting/prompt strings
welcome		BYTE	"><((((> ><((((>	   Welcome to Data Validation, Looping, and Constants! by kevin sekuj	<))))>< <))))><",13,10,0
getName		BYTE	"What's your name? ",0
userName	BYTE	33 DUP(0)				; 32 chars allowed, 33rd for null terminator
greeting	BYTE	"hi, ",0
greetend	BYTE	" :}",13,10,0
guide		BYTE	", please enter negative numbers between [ ",0
guide1		BYTE	" or [ ",0
guide2		BYTE	" ]",0
guideAnd	BYTE	" and ",0
guideEnd	BYTE	"Then, enter a non-negative number to see your results.",13,10,0
extra1		BYTE	"**EC 1: Number the lines during user input, incrementing line number only for valid number entries.",13,10,0
extra2		BYTE	"**EC 2: Calculate and display the average as a decimal-point number, rounded to the nearest .01.",13,10,0

; string characters for concatenating sentences
comma		BYTE	", ",0
openPara	BYTE	"(",0
closePara	BYTE	") ",0
decimal		BYTE	".",0
zero		BYTE	"0",0

; user input strings
enterNum	BYTE	"Enter a number: ",0
numsOK		BYTE	"You entered ",0
numsOK2		BYTE	" valid numbers.",13,10,0
displayMin	BYTE	"The minimum valid number is: ",0
displayMax	BYTE	"The maximum valid number is: ",0
displaySum	BYTE	"The sum of your valid numbers is: ",0
displayAvg	BYTE	"Your rounded average is: ",0
displayDec	BYTE	", or rounded to the hundredths-place: ",0
numsBad		BYTE	"Your number was invalid - try again",13,10,0
numsNoneOK	BYTE	"you didn't enter any valid numbers.... :{",13,10,0
bye			BYTE	"Bye, ",0

; vars for base program calculation
avg			SDWORD	?		
remainder	SDWORD	?		
accum		SDWORD	?		; sum
max			SDWORD	?		
min			SDWORD	?		
counter		DWORD	?		; counter - holds amount of nums entered, i.e the divisor
counterHalf	DWORD	?		; counter divided by 2, used in rounding logic 

; EC2
avgNR		SDWORD	?		; (average not rounded) holds unrounded avg for display as a decimal
roundedDec	SDWORD	?		;  holds rounded decimal value, to the hundredths place
displayZero	DWORD	0		; "bool" to check whether to display an extra 0 in avg
tenthsPlace	DWORD	0		; "bool" to check whether to display a 0 in tenths place, i.e for -1.09

; EC1
lines		DWORD	1		; counting valid input lines 

loopVar		DWORD	?		; to handle input loop

.code
main PROC
	
;-------------------------------------------------------------
;		1.  Program introduction									
;																	
;	Displays the title of the program, the author's name, and the EC
;	options selected. Asks the user for their name and greets them,
;	and then displays the program's instructions.	
;
;-------------------------------------------------------------
	
	; greeting + EC prompts
	mov		edx, offset welcome 
	call	WriteString
	call	CrLf
	mov		edx, offset extra1
	call	WriteString
	mov		edx, offset extra2
	call	WriteString
	call	CrLf

	; get user's name into userName
	mov		edx, offset getName
	call	WriteString
	mov		edx, offset userName
	mov		ecx, sizeof userName
	call	ReadString
	call	CrLf

	; greet the user with their name
	mov		edx, offset	greeting
	call	WriteString
	mov		edx, offset userName
	call	WriteString
	mov		edx, offset greetend
	call	WriteString
	call	CrLf

	; display instructions to user 
	; with negative number range limits
	mov		edx, offset userName
	call	WriteString
	mov		edx, offset guide
	call	WriteString
	mov		eax, LIMIT_LOWER			; displays constants as ints rather than
	call	WriteInt					; hardcoded strings, to account for user
	mov		edx, offset comma			; changing number ranges later on
	call	WriteString
	mov		eax, LIMIT_LOWERMID
	call	WriteInt

	; continuing instructions 
	mov		edx, offset guide2
	call	WriteString
	mov		edx, offset guide1
	call	WriteString
	mov		eax, LIMIT_UPPERMID
	call	WriteInt
	mov		edx, offset comma			; ',' 
	call	WriteString
	mov		eax, LIMIT_UPPER
	call	WriteInt

	; continuing instructions
	mov		edx, offset guide2
	call	WriteString
	call	CrLf
	mov		edx, offset guideEnd
	call	WriteString
	call	CrLf

	mov		loopVar, ecx				; var to handle program loop



_UserInput:

;-------------------------------------------------------------
;		2. Read the user's number inputs									
;		
;	Gets the user's input and checks them against the constant limits 
;	to ensure they're valid inputs. If the user inputs a positive int,
;	jns will read the sign flag and jump to end the program loop and
;	display their calculations or a special parting message for no valid
;	inputs.
;
;-------------------------------------------------------------
	
	; Representing lines input: (lines), i.e (1) 
	mov		edx, offset openPara
	call	WriteString
	mov		eax, lines					; var holding number of valid lines
	call	WriteDec
	mov		edx, offset closePara
	call	WriteString

	; checking if user input num is ns/positive
	mov		edx, offset enterNum
	call	WriteString
	call	ReadInt
	jns		_PosInput					; proceeds to exit if pos num input


	; invalid if lesser than smallest limit
	mov		ebx, LIMIT_LOWER
	cmp		eax, ebx
	jl		_InvalidNum

	; invalid if greater than lower-middle limit, i.e >-100
	xor		ebx, ebx
	mov		ebx, LIMIT_LOWERMID
	cmp		eax, ebx
	jg		_NumCheck

	jmp		_Calculate
	

_NumCheck:
;-------------------------------------------------------------
;		2b. Further input validation									
;		
;	If a number between the two lower limits is given, there is no need
;	to run through all the conditionals, so the program will jump to 
;	calculations to sum the number and append the count. Otherwise, if a
;	negative number greater than the two upper limits is given, the program
;	will jump to _NumCheck to process them. 	
;
;-------------------------------------------------------------
	
	; jmp to display invalid number message if less than 2nd upper limit
	xor		ebx, ebx
	mov		ebx, LIMIT_UPPERMID
	cmp		eax, ebx
	jl		_InvalidNum

	; ditto, but for upper limit (i.e -1)
	xor		ebx, ebx
	mov		ebx, LIMIT_UPPER
	cmp		eax, ebx
	jg		_InvalidNum

	jmp		_Calculate						; jumps to _Calculate if num is valid 

_InvalidNum:
	; writes error and jumps to input loop if user num out of range

	mov		edx, offset numsBad
	call	WriteString

	jmp		_UserInput						; back to input loop



_Calculate:
;-------------------------------------------------------------
;		3. Accumulate user's valid input numbers									
;		
;	Adds the user's valid inputs to accum on each input,
;	holding the sum of valid negative inputs. The counter var is 
;	incremented to represent the count of valid numbers input, and 
;	the lines var is also incremented from its initialized value of 1, 
;	to number the user's valid inputs. 
;	
;	On first input, the program will jump to _SetMaxInit to set the 
;	initial maximum value, which is always the first number entered.  
;
;-------------------------------------------------------------
	
	inc		counter
	inc		lines
	add		accum, eax

	mov		ebx, 1
	cmp		counter, ebx			; set max equal to first input number
	je		_SetMaxInit				



;-------------------------------------------------------------
;		3b. Checking the number against minimum and maximum									
;		
;	The max/min vars will be compared to current input number
;	in the _MaxRange and _MinRange labels. If the number is greater
;	or lesser, the program will then jump to _SetMin or _SetMax to 
;	update the min or max, depending on the outcome of the checks.
;
;-------------------------------------------------------------


_MaxRange:
	; compares max to current user num. If num is greater than current max,
	; it jumps to _SetMax, otherwise, continues.

	xor		ebx, ebx
	mov		ebx, max
	cmp		eax, ebx
	jg		_SetMax
	
_MinRange:
	; compares max to current user num. If num is lesser than current min,
	; it jumps to _SetMin. Otherwise, min/max checks are done - back to user input.

	xor		ebx, ebx
	mov		ebx, min
	cmp		eax, ebx
	jl		_SetMin
	
	jmp		_UserInput				
								

_SetMaxInit:
	; Setting the initial maximum, equal to the first number input, and jumping
	; back to the minimum check afterwards.

	mov		max, eax
	jmp		_MinRange				


_SetMax:
	; Setting new max if necessary, and jumping back to check the minimum

	mov		max, eax
	jmp		_MinRange

_SetMin:
	; Setting new min if necessary, and jumping back to input loop since 
	; min/max checks and updates are finished now

	mov		min, eax
	jmp		_UserInput



;-------------------------------------------------------------
;		4. Loop end, calculating user input nums  									
;		
;	Program will jump to _PosInput when a positive num is 
;	detected. A special check will be done to see if no valid numbers
;	were input and will display a message and end the program, otherwise,
;	it will move on to display results.
;
;-------------------------------------------------------------


_PosInput:
	; checks if counter is 0, i.e, holds no valid inputs, and jumps
	; to _NoValidInput. Otherwise, jumps to display results.

	mov		eax, 0
	cmp		eax, counter
	je		_NoValidInput
	jmp		_ProgramEnd

_NoValidInput:
	; Displays a special parting message for no valid inputs and ends program.

    call	CrLf
	mov		edx, offset numsNoneOK
	call	WriteString
	jmp		ExitProcess



;-------------------------------------------------------------
;		4b. Calculating the average(s)								
;		
;	Calculates the rounded average of the user input numbers, storng
;	results in avg. avg's value is then moved into avgNR, meaning
;	averageNotRounded, which is used in the logic for calculating the
;	rounded decimal place.
;	
;-------------------------------------------------------------
	

_ProgramEnd:
	; Calculates average via IDIV, dividing the sum (accum) of nums
	; with the amount of nums entered (count).

	xor		eax, eax

	mov		eax, accum
	cdq
	mov		ebx, counter
	idiv	ebx
	mov		avg, eax
	mov		avgNr, eax					; stores unrounded average for decimal place calc
	mov		remainder, edx


_TenthsPlaceCheck:
	; Label for the special case where division results in a 0 in the tenths spot, but a number
	; in the hundredths spot, such as 12/11 = 1.09. 


	cmp		remainder, 0				; skips the label if remainder is 0 (to not divide by 0)
	je		_RoundingCalculation


	; if divisor / remainder >= 10, jump to _TenthsPlace immediately
	; Algorithm written with the idea for a quotient result of .01->.09,
	; the divisor must be >90% of the dividend,
	; like in the case of 12/11.

	mov		eax, counter
	mov		edx, 0
	mov		ebx, remainder
	div		ebx
	cmp		edx, 10
	jge		_TenthsPlace


_RoundingCalculation:
	; Handles rounding for the average.

	; Divides the counter, which is the divisor, by 2, for rounding logic
	xor		eax, eax
	xor		ebx, ebx

	mov		eax, counter
	mov		edx, 0
	mov		ebx, 2
	div		ebx
	mov		counterHalf, eax


	; Jumps to rounding logic if the remainder is < divisor/2. This algorithm is 
	; flipped using NEG from the general algo (remainder > divisor/2) so it can be
	; applicable to negative numbers.

	xor		ebx, ebx
	mov		ebx, remainder
	neg		ebx
	cmp		eax, ebx				
	jl		_RoundAvg

	jmp		_Decimal				; jumping to rounding the hundredths place for ec2

	
_RoundAvg:
	; Logic for rounding "up" (decreasing negative by 1). Jumps to _Decimal to handle
	; the hundredths place.

	dec		avg
	jmp		_Decimal

_TenthsPlace:
	; If the calculation results in a number like -1.09 where the tenths spot holds a 0
	; and the hundredths spot holds an integer, then the tenthsPlace "bool" is incremented
	; for use in displaying correct results.

	inc		tenthsPlace
	jmp		_RoundingCalculation	; jumps back up to rounding calculations to continue program



;-------------------------------------------------------------
;		4c. Calculating the average to the hundredths place							
;		
;	Multiplies the IDIV remainder by -100 to get a positive whole number representing
;	a hundredths place digit, storing the result in roundedDec. roundedDec is then
;	divided by counter, the count of numbers input, and jumps to _RoundDecimal if the
;	decimal is greater than 50. 
;
;	Otherwise, it checks if the decimal equals just 0, i.e 3.0, and jumps in that case to represent
;	two 0's in the hundredths place, i.e 3.00. 
;	
;	Otherwise, program moves on to display results.
;
;-------------------------------------------------------------



_Decimal:
	; Multiplying IDIV remainder by -100 to get a positive double digit whole number,
	; i.e remainder of -1 -> 100. This can then be manipulated to get a rounded decimal.

	mov		eax, -100
	mul		remainder
	mov		roundedDec, eax				; storing result in roundedDec
	xor		eax, eax
	xor		ebx, ebx
	xor		edx, edx


	; Dividing roundedDec by number of valid inputs (counter)
	mov		eax, roundedDec
	mov		ebx, counter
	div		ebx							
	mov		roundedDec, eax
	mov		remainder, edx


	; if the result is >50, jump to _RoundDecimal to round the 
	; hundredths place up
	mov		ebx, 50
	cmp		eax, ebx
	jg		_RoundDecimal


	; if the result is just 0, jump to _AddZero to add string 0 
	; for proper hundredths place representation
	mov		ebx, 0
	cmp		eax, ebx
	jz		_AddZero

	jmp		_DisplayResults				; if not rounded up and not == 0, move on
	

_RoundDecimal:
	; Increments the hundredths place, and checks if it is zero as that code segment 
	; would have been skipped in this case. Then, moves onto results

	inc		roundedDec

	mov		ebx, 0
	cmp		ebx, eax
	jz		_AddZero

	jmp		_DisplayResults

_AddZero:
	; displayZero is a "bool" initialized to 0. If the decimal remainder equals 0,
	; the "bool" is set to "True", i.e incremented to 1.

	inc		displayZero


;-------------------------------------------------------------
;		5. Displaying program results							
;		
;	Program results are displayed, including number of valid inputs, min
;	max, sum, average, and average as a decimal-point number. This section
;	contains three logical blocks for displaying the result text and values,
;	and two sections for displaying the decimal remainder, which are discussed 
;	in the next section block.
;
;-------------------------------------------------------------


_DisplayResults:
	; Displaying the basic program requirements such as number of valid inputs and a rounded
	; average.


	; Displays the valid numbers text along with the count of valid nums input
	call	CrLf
	mov		edx, offset numsOK
	call	WriteString
	xor		eax, eax
	mov		eax, counter
	call	WriteDec
	mov		edx, offset numsOK2
	call	WriteString
	call	CrLf

	; Displays the maximum text along with the max value
	mov		edx, offset displayMax
	call	WriteString
	xor		eax, eax
	mov		eax, max
	call	WriteInt
	call	CrLf
	
	; Displays the minimum text along with the min value
	mov		edx, offset displayMin
	call	WriteString
	xor		eax, eax
	mov		eax, min
	call	WriteInt
	call	CrLf

	; Displays the sum text along with accum, the sum variable
	mov		edx, offset displaySum
	call	WriteString
	mov		eax, eax
	mov		eax, accum
	call	Writeint
	call	CrLf

	; Displays the average as a rounded number
	mov		edx, offset displayAvg
	call	WriteString
	mov		eax, eax
	mov		eax, avg
	call	WriteInt


;-------------------------------------------------------------
;		5b. Displaying rounded decimal results							
;		
;	_DisplayDecimal is a continuation of displaying results. In this section,
;	the original unrounded average (avgNR) is printed along with roundedDec,
;	the rounded "hundredths" place number calculated in 4c. 
;
;	This block also handles a tenths place zero plus a num, like -1.09, or a case where
;	the result has only one zero, like -3.0.
;
;-------------------------------------------------------------

_DisplayDecimal:
	; Displaying the rounded decimal result for EC 2. 

	; checking if tenthsPlace is "True", and jumping to _TenthsPlaceZero if so
	xor		eax, eax
	xor		ebx, ebx
	mov		eax, tenthsPlace
	mov		ebx, 1
	cmp		eax, ebx
	je		_TenthsPlaceZero

	; checking if displayZero is "True", and jumping to _DisplayZero if so.
	; these cases will not interfere due to the algorithms used
	xor		eax, eax
	xor		ebx, ebx
	mov		eax, displayZero
	mov		ebx, 1
	cmp		eax, ebx
	je		_DisplayZero
	
	; otherwise, prints the results along with the average rounded to the
	; hundredths place.
	mov		edx, offset DisplayDec
	call	WriteString
	mov		eax, avgNR					; unrounded average, left of radix
	call	WriteInt
	mov		edx, offset decimal
	call	WriteString
	mov		eax, roundedDec
	call	WriteDec

	jmp _Farewell						; jumps to parting message, exits program

_DisplayZero:
	;  Section for writing a string 0 to represent cases where the result of a rounded
	;  decimal is just zero, i.e 3.0 -> 3.00

	mov		edx, offset DisplayDec
	call	WriteString
	mov		eax, avgNR
	call	WriteInt
	mov		edx, offset decimal
	call	WriteString
	mov		eax, roundedDec				; rounded decimal result, in this case, 0
	call	WriteDec
	mov		edx, offset zero			; "0"
	call	WriteString					; .00

	jmp		_Farewell

_TenthsPlaceZero:
	;  Section for writing a string 0 in front of the tenths place, in cases 
	;  such as a result of 1.09. 

	mov		edx, offset DisplayDec
	call	WriteString
	mov		eax, avgNR					; unrounded average
	call	WriteInt
	mov		edx, offset decimal
	call	WriteString
	mov		edx, offset zero			; "0"
	call	WriteString					
	mov		eax, roundedDec				; ".0x"
	call	WriteDec


;-------------------------------------------------------------
;		6. Farewell // Program end							
;		
;	A simple farewell message is printed and the program exits. If this
;	code is executed, then the user input at least one valid number. A
;   special exit case for no valid numbers was handled above.
;
;-------------------------------------------------------------

_Farewell:
	; Prints a farewell message with the user's name and exits the program.

	call	Crlf
	call	Crlf
	mov		edx, offset bye
	call	WriteString
	mov		edx, offset userName
	call	WriteString
	call	CrLf


	Invoke ExitProcess,0	; exit to operating system
main ENDP

; (insert additional procedures here)

END main
