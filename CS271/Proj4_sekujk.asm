TITLE Project Four: Nested Loops, Procedures     (Proj4_sekujk.asm)

; Author: Kevin Sekuj
; Last Modified: 2/21/21
; OSU email address: sekujk@oregonstate.edu
; Course number/section:   CS271 Section 400_W2021
; Project Number: 4                Due Date: 02/21/2021
; Description: Program which calculates prime numbers, first prompting a user
; to enter the number of primes they want displayed in a range of 1 -> 4000. 
; if their input number is verified, the primes of all numbers up to and including
; the nth prime are displayed, 10 primes per line, ascending, with proper spacing and 
; alignment for each prime. New pages are displayed at 20 rows of 10 primes.
; However if the user doesn't enter a valid input, they're reprompted until they
; do so.

INCLUDE Irvine32.inc

; range constants
RANGE_LOWER	= 1			
RANGE_UPPER	= 4000

.data

; introduction vars
greeting		BYTE	"		/¯\_/^_^\_/¯\	 Welcome to Prime Numbers! by kevin sekuj    /¯\_/^_^\_/¯\",13,10,0
prompt			BYTE	"Enter the number of prime numbers you would like to see -"
				BYTE	 " I'll accept up to ",0
prompt1			BYTE	 " primes.",13,10,0
extra1			BYTE	 "**EC 1: Align the output columns, matching first digit offset each row",13,10,0
extra2			BYTE	 "**EC 2: Extend primes range to display up to 4000, 20 rows per page, continuing with any key.",13,10,0

; strings for getUserData
enterData		BYTE	"Enter the number of primes to display: ",0
bracket			BYTE	"[",0
bracket2		BYTE	"]:  ",0
period			BYTE	" ... ",0
error			BYTE	"number out of range...try again",13,10,0
bye				BYTE	"thanks for using my program!! bye :}",13,10,0
space			BYTE	"	 ",0

; vars for showPrimes & subprocs
userNum			DWORD	?		; holds the user's input integer
counter			DWORD	2		; counter variable incrementing up to userNum
validInput		DWORD	0		; "bool" used for validating user input
numOfPrimes		DWORD	?		;  tracks numbers of primes printed

; ec1 
primesCount		DWORD	0		; counter to track how many nums on a line

; ec2 
rows			DWORD	0
continue		BYTE	"press any key to continue!",0

.code

; ---------------------------------------------------------------------------------
; Name: main
;
; main procedure consisting of procedure calls and inline comments outlining subprocedures. 
;
; ---------------------------------------------------------------------------------

main PROC

	call	introduction
	call	getUserData
	;			validate	 subproc of getUserData for validating user inputs
	call	showPrimes
	;			isPrime		 subproc of showPrimes for displaying primes
	;				format		 subproc of isPrime for formatting new lines/pages
	call	farewell

	Invoke ExitProcess,0	; exit to operating system
main ENDP

; ---------------------------------------------------------------------------------
; Name: introduction
;
;	Displays program information to the user, including author, title, and number of primes the user
;	may input.
;
; Preconditions: none
;	
; Postconditions: none 
;
; Receives:
;	 greeting, extra1, extra2, prompt, prompt1 = strings describing program and its functionality
;	 RANGE_UPPER = upper constant limit
;
; Returns: none
;
; ---------------------------------------------------------------------------------

introduction PROC

	; display greeting and ec prompts
	mov		edx, offset greeting
	call	WriteString
	call	CrLf
	mov		edx, offset extra1
	call	WriteString
	mov		edx, offset extra2
	call	WriteString
	call	CrLf

	; continued
	mov		edx, offset prompt
	call	WriteString
	mov		eax, RANGE_UPPER
	call	WriteDec
	mov		edx, offset prompt1
	call	WriteString
	call	CrLf

	ret
introduction ENDP

; ---------------------------------------------------------------------------------
; Name: getUserData
;  Displays the const limits to the user (set to 1 -> 4000 in this program) and asks them to
;  input a value in that range. If their input is false, it tells them and prompts them to try
;  again. Inputs are checked by the validate subproc call which is described in that procedure comment.
;  On valid input the produre returns and sets a bool validInput to true.	
;
; Preconditions: introduction proc has executed and returned
;
; Postconditions: none
;
; Receives: 
;  prompt variables/strings for formatting = enterData, bracket, bracket2, period
;  constant range limits =  RANGE_LOWER and RANGE_UPPER
;  
; Returns: 
;	validInput = bool for valid user input to end proc
;
; ---------------------------------------------------------------------------------

getUserData	 PROC

_InputLoop:
	; input loop where user's data is input and validated


	; display constant ranges and ask user for valid input data
	mov		edx, offset enterData
	call	WriteString

	mov		edx, offset bracket
	call	WriteString
	mov		eax, RANGE_LOWER
	call	WriteDec
	mov		edx, offset period
	call	WriteString
	mov		eax, RANGE_UPPER
	call	WriteDec
	mov		edx, offset bracket2
	call	WriteString

	call	validate				; validate subproc is called to validate the user's input


	cmp		validInput, 1			; if data returned from validate subproc is valid
	je		_ValidInput				


	loop	_InputLoop				; loops back if their data is invalid

_ValidInput:
	; on validated user input, proc returns and program continues onto showPrimes
	ret

getUserData	 ENDP

; ---------------------------------------------------------------------------------
; Name: validate
;	subprocedure within getUserData, called to validate the user's inputs. compares them against
;	constant limits and displays an error, returning back to the getUserData loop when they're false.
;	otherwise it sets the validInput bool to "true" and returns
;
; Preconditions: user inputs a number after WriteDec call
; 
; Postconditions: changes register eax
;
; Receives: 
;	RANGE_LOWER, RANGE_UPPER = constant variables
;
; Returns:
;	userNum = user input number, number of primes to be calculated/displayed
;	validInput = bool to return getUserData and move on to showPrimes proc
;
; ---------------------------------------------------------------------------------

validate	PROC
	
	; reads integer from user and compares it to const limits
	call	ReadDec
	cmp		eax, RANGE_LOWER
	jl		_InvalidNum
	cmp		eax, RANGE_UPPER
	jg		_InvalidNum

	inc		validInput				; increments validInput and stores user's data in userNum
	mov		userNum, eax
	jmp		_ValidNum


_InvalidNum:
	; displays invalid number msg, moves onto proc return
	mov		edx, offset error
	call	WriteString				; validInput will be 0 so getUserData loops again

_ValidNum:
	; if user's data is valid, validInput == 1
	ret

validate	ENDP

; ---------------------------------------------------------------------------------
; Name: showPrimes
;  Moves user input number into an outer loop, and inner nested loop checks all primes up to that number
;  via modulo division. Successful prime numbers call isPrime to write the primes to console with formatting 
;
; Preconditions: user input number (positive between const limits) validated and placed into ecx
; 
; Postconditions: changes registers eax, ebx, ecx
;
; Receives: 
;	userNum = user input number
;	counter = var for every num up to user input number, starting at 2
;
; Returns: counter
;			ebx = divisor
;
; ---------------------------------------------------------------------------------

showPrimes	PROC

	call	CrLf

	mov		ecx, userNum			
	mov		ebx, 2					; ebx used as divisor, initialized to 2

_CountingLoop:
	; userNum moved into ecx and inner loop calculates and displays primes, at which point
	; ecx is decremented in the main CountingLoop until 0


; -----------------------------------------
; Innerloop calculates and displays primes using div. 
; if a num % ebx == 0, it's not prime, and counter is incremented to another number.

; ebx, the divisor, also increments each number up to counter e.g. 5/2..5/3..5/4
; when counter == ebx, then all divisors up to counter have been "exhausted" so it's
; a prime number.
;
; ------------------------------------------
_InnerLoop:	
	; inner nested loop calculating primes, calling isPrime when found

	mov		eax, counter		
	cmp		eax, ebx
	je		_WritePrime			; when counter == ebx, the number is prime
		
	mov		edx, 0
	div		ebx
	cmp		edx, 0				; num % 2 == 0 is not prime		
	je		_NotPrime	

	inc		ebx					; else, increment divisor and restart loop
	jmp		_InnerLoop

_WritePrime:
	; isPrime called with successful prime numbers 
	call	isPrime
	jmp		_Continue

_NotPrime:
	; increment counter to next number, reset divisor (ebx) back to 2
	inc		counter
	mov		ebx, 2
	jmp		_InnerLoop
	
_Continue:	
	; label for looping back to counting loop, decrementing ecx

	loop	_CountingLoop				

	ret
showPrimes	ENDP

; ---------------------------------------------------------------------------------
; Name: isPrime (subprocedure)
;	Subprocedure called by showPrimes on valid prime numbers up to user input N. displays the 
;	number (counter) with proper alignment and calls subproc formatLine when numbers exceed 
;	10 in a row. increments counter when finished (to check next number) and resets ebx (divisor).
;
;
; Preconditions: a valid prime number is found in showPrimes proc.
; 
; Postconditions: changes registers eax, ebx
;
; Receives: 
;	counter = current prime number to be displayed
;	numOfPrimes = holds number of prime numbers displayed, to be cmp with userNum later 
;	primesCount = count of prime numbers on a line
;
; Returns:
;	counter
;	ebx = divisor
;
; ---------------------------------------------------------------------------------

isPrime		PROC
	
	; writes prime number (in counter) to screen along with alignment 
	mov		eax, counter
	call	WriteDec
	mov		edx, offset space		; for alignment
	call	WriteString
	inc		numOfPrimes				

	inc		primesCount				; counter for number of primes on a console line
	cmp		primesCount, 10			
	je		_NewLine				; display new line after 10 primes displayed

	jmp		_IsPrimeEnd

_NewLine:
	; calls formatLine subprocedure to display new console line after 10 primes 
	; are displayed

	call	formatLine

_IsPrimeEnd:
	; handles proc return, incs counter to next num and resets ebx
	inc		counter
	mov		ebx, 2

	ret
isPrime		ENDP

; ---------------------------------------------------------------------------------
; Name: formatLine (subprocedure)
;	Sub-subprocedure of showPrimes/isPrimes to handle new line displays for 10 numbers on a line
;	and create a new screen after 20 rows on a page using ClrScr irvine library procedure. Compares
;	numOfPrimes to userNum to end the program when necessary, otherwise the user would have to enter
;	a new page just to see farewell message printed.
;
; Preconditions: primesCount (num of primes on a given line) = 10 
; 
; Postconditions: changes register AL
;
; Receives:
;	primesCount = number of primes on a line
;	rows = increments after a new line
;	userNum = user input number
;	numOfPrimes = counts the number of primes input
;	
; Returns:
;	primesCount = to 0 after a new line
;	rows = incremented on each new line
;	numOfPrimes = cmp to userNum, end program if equal	
;
; ---------------------------------------------------------------------------------

formatLine	PROC

	call	CrLf
	mov		primesCount, 0			; resets primesCount after a new line
	inc		rows					
	cmp		rows, 20
	je		_NextPage				; display new page at 20 rows

	jmp		_ContDisplay			

_NextPage:
	; display new page using Clrscr library procedure and ask user
	; to press any key to continue.

	mov		rows, 0					; resets rows after a new page

	; to program end if # primes == num input by user
	mov		eax, numOfPrimes
	mov		ebx, userNum
	cmp		eax, ebx
	je		_PartingMessage

	; asks user to press any key to display a new page
	call	CrLf
	mov		edx, offset continue
	call	WriteString
	call	CrLf
	call	ReadChar			
	cmp		AL, ' '				
	call	Clrscr

	jmp		_ContDisplay

_PartingMessage:
	; calls farewell procedure and jumps to end program once done

	call	farewell
	jmp		ExitProcess

_ContDisplay:
	; returns procedure if program will continue

	ret
formatLine	ENDP

; ---------------------------------------------------------------------------------
; Name: farewell
;
; Displays a parting message to the user.
; 
; Preconditions: user input number in ECX concludes its counting loop and showPrimes proc
; returns. Or, in the case of a displaying a new page, userNum is equal to numOfPrimes, which
; is functionally for the same reason.
;
; Receives:
; bye = string "goodbye" message
; ---------------------------------------------------------------------------------

farewell	PROC
	; print farewell message
	call	CrLf
	call	CrLf
	mov		edx, offset bye
	call	WriteString

	ret
farewell	ENDP

END main
