/*--------------------------------------------------------------------------*/
#ifndef WMM_POINT_SUB_H
#define WMM_POINT_SUB_H

/*---------------------------------------------------------------------------*/

/* 
WMM Point Calculation Program.

The Geomagnetism Library is used to make a command prompt program. The program prompts
the user to enter a location, performs the computations and prints the results to the
standard output. The program expects the files GeomagnetismLibrary.c, GeomagnetismHeader.h,
WMM.COF and EGM9615.h to be in the same directory. 

Manoj.C.Nair@Noaa.Gov
April 21, 2011

 *  Revision Number: $Revision: 1270 $
 *  Last changed by: $Author: awoods $
 *  Last changed on: $Date: 2014-11-21 10:40:43 -0700 (Fri, 21 Nov 2014) $
 */
int wmmsub(double geolatitude, double geolongitude, double HeightAboveEllipsoid, double yeardecimal,
              double* X, double* Y, double* Z, double* F, double* Decl, double* Incl, char* filename);

#endif  // WMM_POINT_SUB_H
