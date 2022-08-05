TITLE Project 1, Basic Logic and Arithmetic Program     (Proj1_sekujk.asm)

; Author: Kevin Sekuj
; Last Modified: 1/16/2021
; OSU email address: sekujk@oregonstate.edu
; Course number/section:   CS271 Section 400_W2021
; Project Number: 1				Due Date: 1/24/21
; Description: Logic and arithmetic program, which takes 3 user input integers 
; in descending order and calculates basic mathematical operations, such as 
; addition, subtraction, and division. Additionally, the program will loop 
; until the user chooses to exit.

INCLUDE Irvine32.inc


.data

intro		BYTE	"		---{{@    Basic Logic and Arithmetic Program by Kevin Sekuj    @}}---",0
extraCred1	BYTE	"**EC: 1. Repeat until the user chooses to quit",0
extraCred2	BYTE	"**EC: 2. Check if numbers are in non-descending order",0
extraCred3	BYTE	"**EC: 3. Handle negative results and computes B-A, C-A, C-B, C-B-A",0
extraCred4	BYTE	"**EC: 4. Calculate and display the quotients A/B, A/C, B/C, printing the quotient and remainder",0
prompt		BYTE	"Enter 3 numbers (A>B>C) in descending order, and I'll show you their sums, differences, and quotients!",0
firstNum	BYTE	"First number: ",0
secondNum	BYTE	"Second number: ",0
thirdNum	BYTE	"Third number: ",0
plusText	BYTE	" + ",0
subText		BYTE	" - ",0
divText		BYTE	" / ",0
remainder	BYTE	" with a remainder of: " ,0
equalText	BYTE	" = ",0
quit		BYTE	"Press  y  to continue, otherwise any other key will exit the program.",0
wrongOrder	BYTE	"Error: the numbers are in non-descending order! Try again.",0
goodbye		BYTE	"Thanks for using elementary arithmetic!  bye!!! ~ :)",0

numA		DWORD	?		; user input numbers
numB		DWORD	?
numC		DWORD	?

aSumB		DWORD	?		; addition identifiers
aSubB		DWORD	?
aSumC		DWORD	?
aSubC		DWORD	?
bSumC		DWORD	?
bSubC		DWORD	?
sumABC		DWORD	?

bSubA		DWORD	?		; subtraction identifiers
cSubA		DWORD	?
cSubB		DWORD	?
subCBA		DWORD	?

abQuotient	DWORD	?		; division identifiers
abRem		DWORD	?
acQuotient	DWORD	?
acRem		DWORD	?
bcQuotient	DWORD	?
bcRem		DWORD	?

loopVar		DWORD	?		; to handle program loop


.code
main PROC

;------------------------------------------------------------
;		1. Introduction to program:									
;																	
;	Displays the title of the program and the author, displays			
;	the extra credit options seelected. Then, it displays a prompt	
;	for three integers in descending order.							
;------------------------------------------------------------

	mov		EDX, OFFSET intro
	call	WriteString
	call	CrLf
	mov		EDX, OFFSET extraCred1
	call	WriteString
	call	CrLf
	mov		EDX, OFFSET extraCred2
	call	WriteString
	call	CrLf
	mov		EDX, OFFSET extraCred3
	call	WriteString
	call	CrLf
	mov		EDX, OFFSET extraCred4
	call	WriteString
	call	CrLf
	call	CrLf
	mov		EDX, OFFSET prompt
	call	WriteString
	call    CrLf

_UserInput:							; start point for program loops, or restarts for invalid input

;-------------------------------------------------------------
;		2. Gets the user's data:									
;																	
;	Gets user input integers and stores them in memory variables.	
;	Checks user nums are in descending order with jle, and jumps to	
;	 _UserInput label if they aren't. Stores loop variable in ECX.	
;-------------------------------------------------------------

	mov		loopVar, ECX
	
	call	CrLf
	mov		EDX, OFFSET firstNum
	call	WriteString
	call	ReadInt
	mov		numA, EAX

	mov		EDX, OFFSET secondNum
	call	WriteString
	call	ReadInt
	mov		numB, EAX

	; checking if num C <= B <= A (descending order)
	; if invalid input, jumps back to _OrderError
	xor		EAX, EAX				
	xor		EBX, EBX				
	mov		EAX, numA
	mov		EBX, numB
	cmp		EAX, EBX
	jle		_OrderError

	mov		EDX, OFFSET thirdNum
	call	WriteString
	call	ReadInt
	mov		numC, EAX
	call	CrLf

	xor		EAX, EAX
	xor		EBX, EBX
	mov		EAX, numB
	mov		EBX, numC
	cmp		EAX, EBX
	jle		_OrderError

	xor		EAX, EAX
	xor		EBX, EBX
	mov		EAX, numA
	mov		EBX, numC
	cmp		EAX, EBX
	jle		_OrderError

	jmp		_continue				; jumps to _continue if user's inputs are valid

_OrderError:					 
	; displays error msg for invalid input, jumps to _UserInput to restart

	mov		EDX, OFFSET wrongOrder
	call	WriteString
	call	crLf
	jmp		_UserInput

_continue:

;--------------------------------------------------------
;		3. Calculate the required values:							
;																	
;	Calculates sums, differences, differences, quotients, and		
;	remainders of user num variables, storing the results in		
;	other variables.												
;--------------------------------------------------------

	; Calculating sum of integers
	mov		EAX, numA			
	mov		EBX, numB
	add		EAX, EBX
	mov		aSumB, EAX

	mov		EAX, numA
	mov		EBX, numB
	sub		EAX, EBX
	mov		aSubB, EAX

	mov		EAX, numA
	mov		EBX, numC
	add		EAX, EBX
	mov		aSumC, EAX

	mov		EAX, numA
	mov		EBX, numC
	sub		EAX, EBX
	mov		aSubC, EAX

	mov		EAX, numB
	mov		EBX, numC
	add		EAX, EBX
	mov		bSumC, EAX

	mov		EAX, numB
	mov		EBX, numC
	sub		EAX, EBX
	mov		bSubC, EAX

	mov		EAX, aSumC
	mov		EBX, numB
	add		EAX, EBX
	mov		sumABC, EAX

	; Calculating difference of integers
	mov		EAX, numB
	mov		EBX, numA
	sub		EAX, EBX
	mov		bSubA, EAX

	mov		EAX, numC
	mov		EBX, numA
	sub		EAX, EBX
	mov		cSubA, EAX

	mov		EAX, numC
	mov		EBX, numB
	sub		EAX, EBX
	mov		cSubB, EAX

	mov		EAX, numC
	mov		EBX, numB
	sub		EAX, EBX
	mov		cSubB, EAX

	mov		EAX, cSubB
	mov		EBX, numA
	sub		EAX, EBX
	mov		subCBA, EAX

	; Calculating quotients and remainders
	mov		EAX, numA
	mov		EDX, 0 
	mov		EBX, numB
	div		EBX 
	mov		abRem, EDX				; ab rem = remainder of A / B
	mov		abQuotient, EAX

	mov		EAX, numA
	mov		EDX, 0
	mov		EBX, numC
	div		EBX
	mov		acRem, EDX
	mov		acQuotient, EAX

	mov		EAX, numB
	mov		EDX, 0
	mov		EBX, numC
	div		EBX
	mov		bcRem, EDX
	mov		bcQuotient, EAX

;----------------------------------------------------------
;		4. Displaying the results:									
;																	
;	Displays the results of addition, subtraction, as well as		
;	division, concatenating the integer variables with operator		
;	strings like "+" to display a full operation.					
;----------------------------------------------------------

	; Addition & Subtraction

	; A + B = sum(A, B)
	mov		EAX, numA 
	call	WriteDec
	mov		EDX, OFFSET plusText		; ' + '
	call	WriteString
	mov		EAX, numB
	call	WriteDec
	mov		EDX, OFFSET equalText		; ' = '
	call	WriteString
	mov		EAX, aSumB
	call	WriteDec
	call	CrLf

	; A - B = difference(A, B)
	mov		EAX, numA 
	call	WriteDec
	mov		EDX, OFFSET subText			; ' - '
	call	WriteString
	mov		EAX, numB
	call	WriteDec
	mov		EDX, OFFSET equalText
	call	WriteString
	mov		EAX, aSubB
	call	WriteDec
	call	CrLf

	; A + C = sum(A, C)
	mov		EAX, numA 
	call	WriteDec
	mov		EDX, OFFSET plusText
	call	WriteString
	mov		EAX, numC
	call	WriteDec
	mov		EDX, OFFSET equalText
	call	WriteString
	mov		EAX, aSumC
	call	WriteDec
	call	CrLf

	; A - C = difference(A, C)
	mov		EAX, numA
	call	WriteDec
	mov		EDX, OFFSET subText
	call	WriteString
	mov		EAX, numC
	call	WriteDec
	mov		EDX, OFFSET equalText
	call	WriteString
	mov		EAX, aSubC
	call	WriteDec
	call	CrLf

	; B + C = sum(B, C)
	mov		EAX, numB 
	call	WriteDec
	mov		EDX, OFFSET plusText
	call	WriteString
	mov		EAX, numC
	call	WriteDec
	mov		EDX, OFFSET equalText
	call	WriteString
	mov		EAX, bSumC
	call	WriteDec
	call	CrLf

	; B - C = difference(B, C)
	mov		EAX, numB 
	call	WriteDec
	mov		EDX, OFFSET subText
	call	WriteString
	mov		EAX, numC
	call	WriteDec
	mov		EDX, OFFSET equalText
	call	WriteString
	mov		EAX, bSubC
	call	WriteDec
	call	CrLf

	; A + B + C = sum(A, B, C)
	mov		EAX, numA
	call	WriteDec
	mov		EDX, OFFSET plusText
	call	WriteString
	mov		EAX, numB
	call	WriteDec
	mov		EDX, OFFSET plusText
	call	WriteString
	mov		EAX, numC
	call	WriteDec
	mov		EDX, OFFSET equalText
	call	WriteString
	mov		EAX, sumABC
	call	WriteDec
	call	CrLf
	call	CrLf
	
	; B - A = difference(B, A)
	mov		EAX, numB
	call	WriteDec
	mov		EDX, OFFSET subText
	call	WriteString
	mov		EAX, numA
	call	WriteDec
	mov		EDX, OFFSET equalText
	call	WriteString
	mov		EAX, bSubA
	call	WriteInt
	call	CrLf

	; C - A = difference(C, A)
	mov		EAX, numC
	call	WriteDec
	mov		EDX, OFFSET subText
	call	WriteString
	mov		EAX, numA
	call	WriteDec
	mov		EDX, OFFSET equalText
	call	WriteString
	mov		EAX, cSubA
	call	WriteInt
	call	CrLf

	; C - B = difference(C, B)
	mov		EAX, numC
	call	WriteDec
	mov		EDX, OFFSET subText
	call	WriteString
	mov		EAX, numB
	call	WriteDec
	mov		EDX, OFFSET	equalText
	call	WriteString
	mov		EAX, cSubB
	call	WriteInt
	call	CrLf

	; C - B - A = difference(C, B, A)
	mov		EAX, numC
	call	WriteDec
	mov		EDX, OFFSET subText
	call	WriteString
	mov		EAX, numB
	call	WriteDec
	mov		EDX, OFFSET subText
	call	WriteString
	mov		EAX, numA
	call	WriteDec
	mov		EDX, OFFSET equalText
	call	WriteString
	mov		EAX, subCBA
	call	WriteInt
	call	CrLf
	call	CrLf

	; Division

	; A / B
	xor		EAX, EAX					; clearing EAX before starting operation
	mov		EAX, numA
	call	WriteDec
	mov		EDX, OFFSET divText			; " / "
	call	WriteString
	mov		EAX, numB
	call	WriteDec
	mov		EDX, OFFSET equalText
	call	WriteString
	mov		EAX, abQuotient
	call	WriteDec
	mov		EDX, OFFSET remainder
	call	WriteString
	mov		EAX, abRem
	call	WriteDec
	call	CrLf

	; A / C
	xor		EAX, EAX
	mov		EAX, numA
	call	WriteDec
	mov		EDX, OFFSET divText
	call	WriteString
	mov		EAX, numC
	call	WriteDec
	mov		EDX, OFFSET equalText
	call	WriteString
	mov		EAX, acQuotient
	call	WriteDec
	mov		EDX, OFFSET remainder
	call	WriteString
	mov		EAX, acRem
	call	WriteDec
	call	CrLf

	; B / C
	xor		EAX, EAX
	mov		EAX, numB
	call	WriteDec
	mov		EDX, OFFSET divText
	call	WriteString
	mov		EAX, numC
	call	WriteDec
	mov		EDX, OFFSET equalText
	call	WriteString
	mov		EAX, bcQuotient
	call	WriteDec
	mov		EDX, OFFSET remainder
	call	WriteString
	mov		EAX, bcRem
	call	WriteDec
	call	CrLf
	call	CrLf

;-------------------------------------------------------------
;		4.a Program loop:											
;																	
;	Asks the user to press 'y' to continue, or exit with any other	
;	key. If they continue, it jumps back to program start.			
;-------------------------------------------------------------
	mov		EDX, OFFSET quit
	call	WriteString
	call	CrLf
	xor		EAX, EAX			; clearing EAX
	call	ReadChar			
	cmp		AL, 'y'				; comparing user input char with 'y' key
	je		_UserInput			; jumps to start of program if user input equals 'y'


;-------------------------------------------------------
;		5. Goodbye message:											
;																	
;	Displays a simple good bye message if the user chooses to		
;	end the program loop and quit.									
;-------------------------------------------------------

	call	CrLf
	mov		EDX, OFFSET goodbye
	call	WriteString
	call	CrLf

	Invoke ExitProcess,0		; exit to operating system
main ENDP


END main
