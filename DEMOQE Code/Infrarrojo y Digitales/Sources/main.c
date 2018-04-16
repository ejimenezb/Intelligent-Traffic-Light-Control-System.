/* ###################################################################
**     Filename    : main.c
**     Project     : Serial
**     Processor   : MC9S08QE128CLK
**     Version     : Driver 01.12
**     Compiler    : CodeWarrior HCS08 C Compiler
**     Date/Time   : 2018-01-22, 14:38, # CodeGen: 0
**     Abstract    :
**         Main module.
**         This module contains user's application code.
**     Settings    :
**     Contents    :
**         No public methods
**
** ###################################################################*/
/*!
** @file main.c
** @version 01.12
** @brief
**         Main module.
**         This module contains user's application code.
*/         
/*!
**  @addtogroup main_module main module documentation
**  @{
*/         
/* MODULE main */


/* Including needed modules to compile this module/procedure */
#include "Cpu.h"
#include "Events.h"
#include "Bit1.h"
#include "TI1.h"
#include "AS1.h"
#include "AD1.h"
#include "Bit2.h"
#include "Bit3.h"
#include "Bit4.h"
#include "Bit5.h"
#include "Bit6.h"
/* Include shared modules, which are used for whole project */
#include "PE_Types.h"
#include "PE_Error.h"
#include "PE_Const.h"
#include "IO_Map.h"

/* User includes (#include below this line is not maintained by Processor Expert) */

unsigned char estado = ESPERAR;
unsigned char CodError;
unsigned char CodError1;
unsigned char CodError2;
unsigned char CodError3;
unsigned char CodError4;

unsigned int unCanal;
unsigned int dosCanales;
unsigned int tresCanales;

//unsigned char ctrama[3] = {0xF1, 0x00, 0x00}; //Un sensor analogico con 2 digitales
//unsigned char ctrama[5] = {0xF2, 0x00, 0x00, 0x00, 0x00}; //Dos sensores analogico con 2 digitales
unsigned char ctrama[9] = {0xF4, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}; //Cuatro sensores analogico con 2 digitales

//unsigned int medida;
//unsigned int medida[4] = {0x00, 0x00, 0x00, 0x00};

unsigned int medida1;
unsigned int medida2;
unsigned int medida3;
unsigned int medida4;

unsigned int inutil = 2;


unsigned int D1;
unsigned int D2;
unsigned int D3;
unsigned int D4;
unsigned int D5;
unsigned int D6;
unsigned int D7;
unsigned int D8;

void main(void)
{
  /* Write your local variable definition here */
	//unsigned char medida;
	

  /*** Processor Expert internal initialization. DON'T REMOVE THIS CODE!!! ***/
  PE_low_level_init();
  /*** End of Processor Expert internal initialization.                    ***/

  /* Write your code here */
  /* For example: for(;;) { } */
  for(;;){
    
	switch (estado){
  		
  			case ESPERAR:
  			
  				break;
  			
  			case MEDIR:
  				
  				CodError = AD1_Measure(TRUE);
  				
  				//CodError = AD1_GetValue16(&medida);   //medida es un entero de 16 bits = 1111101011110000
  				
  				CodError1 = AD1_GetChanValue16(0, &medida1);
  				CodError2 = AD1_GetChanValue16(1, &medida2);
  				CodError3 = AD1_GetChanValue16(2, &medida3);
  				CodError4 = AD1_GetChanValue16(3, &medida4);
  				
  				//Bit2_NegVal();
  				
  				//Protocolo de Comunicacion
  				
  				//---------------------------------------Bits Digitales------------------------------------------------------
  				
  				D1=1;  //Bit5_GetVal();
  				D2=1;  //Bit6_GetVal();
  				D3=0;
  				D4=0;
  				D5=0;
  				D6=0;
  				D7=0;
  				D8=0;
  				
  				//----------------------------------------Un solo canal------------------------------------------------------
  				//ctrama[1] = (medida >> 11) & (0x1F);
  				//D1 = (D1 << 6);
  				//D2 = (D2 << 5);
  				//ctrama[1] = ctrama[1] | D1 | D2;
  				//ctrama[2] = (medida >> 4) & (0x7F);
  				
  				
  				//---------------------------------------Cuatro canales con vector medida[4]---------------------------------
  				/*ctrama[1] = (medida[0] >> 11) & (0x1F);
  				D1 = (D1 << 6);
  				D2 = (D2 << 5);
  				ctrama[1] = ctrama[1] | D1 | D2;
  				ctrama[2] = (medida[0] >> 4) & (0x7F);
  				
  				ctrama[3] = (medida[1] >> 11) & (0x1F);
  				D1 = (D1 << 6);
  				D2 = (D2 << 5);
  				ctrama[3] = ctrama[3] | D1 | D2;
  				ctrama[4] = (medida[1] >> 4) & (0x7F);
  				
  					
  				ctrama[5] = (medida[2] >> 11) & (0x1F);
  				D1 = (D1 << 6);
  				D2 = (D2 << 5);
  				ctrama[5] = ctrama[5] | D1 | D2;
  				ctrama[6] = (medida[2] >> 4) & (0x7F);
  				
  				ctrama[7] = (medida[3] >> 11) & (0x1F);
  				D1 = (D1 << 6);
  				D2 = (D2 << 5);
  				ctrama[7] = ctrama[7] | D1 | D2;
  				ctrama[8] = (medida[3] >> 4) & (0x7F);*/
  				
  				//----------------------------------------------Cuatro canales con variables medida independientes-----------
  				
  				ctrama[1] = (medida1 >> 11) & (0x1F);
  				D1 = (D1 << 6);
  				D2 = (D2 << 5);
  				ctrama[1] = ctrama[1] | D1 | D2;
  				ctrama[2] = (medida1 >> 4) & (0x7F);
  				
  				
  				ctrama[3] = (medida2 >> 11) & (0x1F);
  				D3 = (D3 << 6);
  				D4 = (D4 << 5);
  				ctrama[3] = ctrama[3] | D3 | D4;
  				ctrama[4] = (medida2 >> 4) & (0x7F);
  				
  					
  				ctrama[5] = (medida3 >> 11) & (0x1F);
  				D5 = (D5 << 6);
  				D6 = (D6 << 5);
  				ctrama[5] = ctrama[5] | D5 | D6;
  				ctrama[6] = (medida3 >> 4) & (0x7F);
  				
  				
  				ctrama[7] = (medida4 >> 11) & (0x1F);
  				D7 = (D7 << 6);
  				D8 = (D8 << 5);
  				ctrama[7] = ctrama[7] | D7 | D8;
  				ctrama[8] = (medida4 >> 4) & (0x7F);
  			
  				estado = ENVIAR;
  			  			
  				break;
  	
  			case ENVIAR:
  				
  				//empezar = Bit5_GetVal();
  				
				//if(empezar == 1)
  				//{
  				  				
  				unCanal = Bit2_GetVal();
  				dosCanales = Bit3_GetVal();
  				tresCanales = Bit4_GetVal();
  				
  				if(unCanal == 0 )
  				{
  					ctrama[0] = 0xF1;
  					AS1_SendBlock(ctrama, 3, &inutil);
  				}
  				else if(dosCanales == 0)
  					{ 
  						ctrama[0] = 0xF2;
  						AS1_SendBlock(ctrama, 5, &inutil);
  					}
  					else if(tresCanales == 0)
  						{ 
  							ctrama[0] = 0xF3;
  							AS1_SendBlock(ctrama, 7, &inutil);
  						}else
  							{
  								ctrama[0] = 0xF4;
  								AS1_SendBlock(ctrama, 9, &inutil);	
  							}
  				
  				//}
  				
  				//Bit2_NegVal();
  				estado = ESPERAR;
  			
  				break;
  			
  			default:
  			
  				break;
	  }
  }

  /*** Don't write any code pass this line, or it will be deleted during code generation. ***/
  /*** RTOS startup code. Macro PEX_RTOS_START is defined by the RTOS component. DON'T MODIFY THIS CODE!!! ***/
  #ifdef PEX_RTOS_START
    PEX_RTOS_START();                  /* Startup of the selected RTOS. Macro is defined by the RTOS component. */
  #endif
  /*** End of RTOS startup code.  ***/
  /*** Processor Expert end of main routine. DON'T MODIFY THIS CODE!!! ***/
  for(;;){}
  /*** Processor Expert end of main routine. DON'T WRITE CODE BELOW!!! ***/
  } /*** End of main routine. DO NOT MODIFY THIS TEXT!!! ***/

/* END main */
/*!
** @}
*/
/*
** ###################################################################
**
**     This file was created by Processor Expert 10.3 [05.09]
**     for the Freescale HCS08 series of microcontrollers.
**
** ###################################################################
*/
