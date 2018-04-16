/* ###################################################################
**     Filename    : Events.c
**     Project     : Serial
**     Processor   : MC9S08QE128CLK
**     Component   : Events
**     Version     : Driver 01.02
**     Compiler    : CodeWarrior HCS08 C Compiler
**     Date/Time   : 2018-01-22, 14:38, # CodeGen: 0
**     Abstract    :
**         This is user's event module.
**         Put your event handler code here.
**     Settings    :
**     Contents    :
**         No public methods
**
** ###################################################################*/
/*!
** @file Events.c
** @version 01.02
** @brief
**         This is user's event module.
**         Put your event handler code here.
*/         
/*!
**  @addtogroup Events_module Events module documentation
**  @{
*/         
/* MODULE Events */


#include "Cpu.h"
#include "Events.h"

/* User includes (#include below this line is not maintained by Processor Expert) */

//unsigned char mensaje[3] = {"HEY"};
//unsigned int inutil = 2;

/*
** ===================================================================
**     Event       :  AS1_OnError (module Events)
**
**     Component   :  AS1 [AsynchroSerial]
**     Description :
**         This event is called when a channel error (not the error
**         returned by a given method) occurs. The errors can be read
**         using <GetError> method.
**         The event is available only when the <Interrupt
**         service/event> property is enabled.
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/
void  AS1_OnError(void)
{
  /* Write your code here ... */
}

/*
** ===================================================================
**     Event       :  AS1_OnRxChar (module Events)
**
**     Component   :  AS1 [AsynchroSerial]
**     Description :
**         This event is called after a correct character is received.
**         The event is available only when the <Interrupt
**         service/event> property is enabled and either the <Receiver>
**         property is enabled or the <SCI output mode> property (if
**         supported) is set to Single-wire mode.
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/
void  AS1_OnRxChar(void)
{
  /* Write your code here ... */
}

/*
** ===================================================================
**     Event       :  AS1_OnTxChar (module Events)
**
**     Component   :  AS1 [AsynchroSerial]
**     Description :
**         This event is called after a character is transmitted.
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/
void  AS1_OnTxChar(void)
{
  /* Write your code here ... */
	 		 
		 CodError =  AS1_RecvChar( &estadoSemaforo );
		 estadoComparacion = (estadoSemaforo); //& 0xf0;
		 if ( estadoComparacion == 0x00) {
			 //Semaforo 1
			 Bit12_ClrVal(); //Rojo
			 Bit2_ClrVal(); //Amarillo
			 Bit3_ClrVal(); //Verde
			 //Semaforo 2
			 Bit4_ClrVal(); //Rojo
			 Bit13_ClrVal(); //Amarillo
			 Bit14_ClrVal(); //Verde
		 }else if (estadoComparacion == 0x21){
			 //Semaforo 1
			 Bit12_ClrVal(); //Rojo
			 Bit2_ClrVal(); //Amarillo
			 Bit3_SetVal(); //Verde
			 //Semaforo 2
			 Bit4_SetVal(); //Rojo
			 Bit13_ClrVal(); //Amarillo
			 Bit14_ClrVal(); //Verde
		 }else if (estadoComparacion == 0xc){
			 //Semaforo 1
			 Bit12_SetVal(); //Rojo
			 Bit2_ClrVal(); //Amarillo
			 Bit3_ClrVal(); //Verde
			 //Semaforo 2
			 Bit4_ClrVal(); //Rojo
			 Bit13_ClrVal(); //Amarillo
			 Bit14_SetVal(); //Verde
		 }else if (estadoComparacion == 0x11){
			 //Semaforo 1
			 Bit12_ClrVal(); //Rojo
			 Bit2_SetVal(); //Amarillo
			 Bit3_ClrVal(); //Verde
			 //Semaforo 2
			 Bit4_SetVal(); //Rojo
			 Bit13_ClrVal(); //Amarillo
			 Bit14_ClrVal(); //Verde	 
		 }else if (estadoComparacion == 0xa){
			 //Semaforo 1
			 Bit12_SetVal(); //Rojo
			 Bit2_ClrVal(); //Amarillo
			 Bit3_ClrVal(); //Verde
			 //Semaforo 2
			 Bit4_ClrVal(); //Rojo
			 Bit13_SetVal(); //Amarillo
			 Bit14_ClrVal(); //Verde
		 }else if (estadoComparacion == 0x9){
			 //Semaforo 1
			 Bit12_SetVal(); //Rojo
			 Bit2_ClrVal(); //Amarillo
			 Bit3_ClrVal(); //Verde
			 //Semaforo 2
			 Bit4_SetVal(); //Rojo
			 Bit13_ClrVal(); //Amarillo
			 Bit14_ClrVal(); //Verde
		 }
}

/*
** ===================================================================
**     Event       :  AS1_OnFullRxBuf (module Events)
**
**     Component   :  AS1 [AsynchroSerial]
**     Description :
**         This event is called when the input buffer is full;
**         i.e. after reception of the last character 
**         that was successfully placed into input buffer.
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/
void  AS1_OnFullRxBuf(void)
{
  /* Write your code here ... */
}

/*
** ===================================================================
**     Event       :  AS1_OnFreeTxBuf (module Events)
**
**     Component   :  AS1 [AsynchroSerial]
**     Description :
**         This event is called after the last character in output
**         buffer is transmitted.
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/
void  AS1_OnFreeTxBuf(void)
{
  /* Write your code here ... */
}

/*
** ===================================================================
**     Event       :  TI1_OnInterrupt (module Events)
**
**     Component   :  TI1 [TimerInt]
**     Description :
**         When a timer interrupt occurs this event is called (only
**         when the component is enabled - <Enable> and the events are
**         enabled - <EnableEvent>). This event is enabled only if a
**         <interrupt service/event> is enabled.
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/
void TI1_OnInterrupt(void)
{
  /* Write your code here ... */
	
	if (estado == ESPERAR){
		
		estado = MEDIR;
	}
	
}

/*
** ===================================================================
**     Event       :  AD1_OnEnd (module Events)
**
**     Component   :  AD1 [ADC]
**     Description :
**         This event is called after the measurement (which consists
**         of <1 or more conversions>) is/are finished.
**         The event is available only when the <Interrupt
**         service/event> property is enabled.
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/
void AD1_OnEnd(void)
{
  /* Write your code here ... */
}


/*
** ===================================================================
**     Event       :  Cap1_OnCapture (module Events)
**
**     Component   :  Cap1 [Capture]
**     Description :
**         This event is called on capturing of Timer/Counter actual
**         value (only when the component is enabled - <Enable> and the
**         events are enabled - <EnableEvent>.This event is available
**         only if a <interrupt service/event> is enabled.
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/
void Cap1_OnCapture(void)
{
  /* Write your code here ... */
		
	if (estado_echo1 == ECHO1_TRIGGERED){
				Cap1_Reset(); // Se detecta el Rising edge, resetear registro de captura
				estado_echo1 = ECHO1_MEDIR;
			}
			else if (estado_echo1 == ECHO1_MEDIR){
				Cap1_GetCaptureValue(&medicionUltra1);// Se guarda el valor medido en el Falling edge
				estado_echo1 = ECHO1_TERMINADO;
				Bit9_NegVal();
				}
			else if (estado_echo1 == ECHO1_TERMINADO){

				}
	
}

/*
** ===================================================================
**     Event       :  TI2_OnInterrupt (module Events)
**
**     Component   :  TI2 [TimerInt]
**     Description :
**         When a timer interrupt occurs this event is called (only
**         when the component is enabled - <Enable> and the events are
**         enabled - <EnableEvent>). This event is enabled only if a
**         <interrupt service/event> is enabled.
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/
void TI2_OnInterrupt(void)
{
  /* Write your code here ... */
	
	if (estado_trigger == TRIGGER_TERMINADO){
		}
		else if (estado_trigger == TRIGGER_BAJO){
			Bit7_SetVal();
			Bit10_SetVal();
			//Bit8_ClrVal(); Bandera LED para probar trigger
			estado_trigger = TRIGGER_ALTO;
			}
		else if (estado_trigger == TRIGGER_ALTO){
			Bit7_ClrVal();
			Bit10_ClrVal();
			//Bit8_SetVal(); Bandera LED para probar trigger
			estado_trigger = TRIGGER_TERMINADO;
			}
}

/*
** ===================================================================
**     Event       :  Cap2_OnCapture (module Events)
**
**     Component   :  Cap2 [Capture]
**     Description :
**         This event is called on capturing of Timer/Counter actual
**         value (only when the component is enabled - <Enable> and the
**         events are enabled - <EnableEvent>.This event is available
**         only if a <interrupt service/event> is enabled.
**     Parameters  : None
**     Returns     : Nothing
** ===================================================================
*/
void Cap2_OnCapture(void)
{
  /* Write your code here ... */
	if (estado_echo2 == ECHO2_TRIGGERED){
				Cap2_Reset();// Se detecta el Rising edge, resetear registro de captura
				estado_echo2 = ECHO2_MEDIR;
			}
			else if (estado_echo2 == ECHO2_MEDIR){
				Cap2_GetCaptureValue(&medicionUltra2);// Se guarda el valor medido en el Falling edge
				estado_echo2 = ECHO2_TERMINADO;
				Bit11_NegVal();
				}
			else if (estado_echo2 == ECHO2_TERMINADO){

				}
}

/* END Events */

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
