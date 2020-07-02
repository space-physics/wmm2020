/*--------------------------------------------------------------------------*/

#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>


#include "GeomagnetismHeader.h"
/*#include "GeomagnetismLibrary.c"*/
#include "EGM9615.h"

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
           double* X, double* Y, double* Z, double* F, double* Decl, double* Incl)
{
    MAGtype_MagneticModel * MagneticModels[1], *TimedMagneticModel;
    MAGtype_Ellipsoid Ellip;
    MAGtype_CoordSpherical CoordSpherical;
    MAGtype_CoordGeodetic CoordGeodetic;
    MAGtype_Date UserDate;
    MAGtype_GeoMagneticElements GeoMagneticElements,Errors;
    MAGtype_Geoid Geoid;
    char ans[20], b;
    char filename[] = "WMM.COF";
    char VersionDate_Large[] = "$Date: 2014-11-21 10:40:43 -0700 (Fri, 21 Nov 2014) $";
    char VersionDate[12];
    int NumTerms, Flag = 1, nMax = 0;
    int epochs = 1;
    /* Memory allocation */


    strncpy(VersionDate, VersionDate_Large + 39, 11);
    VersionDate[11] = '\0';
    if(!MAG_robustReadMagModels(filename, &MagneticModels, epochs)) {
        fprintf(stderr,"\n WMM.COF not found.\n");
        return EXIT_FAILURE;
    }
    if(nMax < MagneticModels[0]->nMax) nMax = MagneticModels[0]->nMax;
    NumTerms = ((nMax + 1) * (nMax + 2) / 2);
    TimedMagneticModel = MAG_AllocateModelMemory(NumTerms); /* For storing the time modified WMM Model parameters */
    if(MagneticModels[0] == NULL || TimedMagneticModel == NULL)
    {
        MAG_Error(2);
    }
    MAG_SetDefaults(&Ellip, &Geoid); /* Set default values and constants */
    /* Check for Geographic Poles */



    /* Set EGM96 Geoid parameters */
    Geoid.GeoidHeightBuffer = GeoidHeightBuffer;
    Geoid.Geoid_Initialized = 1;
    Geoid.UseGeoid = 0;
    /* Set EGM96 Geoid parameters END */

    CoordGeodetic.HeightAboveEllipsoid = HeightAboveEllipsoid;
    CoordGeodetic.phi = geolatitude;
    CoordGeodetic.lambda = geolongitude;
    
    UserDate.DecimalYear = yeardecimal;

    MAG_GeodeticToSpherical(Ellip, CoordGeodetic, &CoordSpherical); /*Convert from geodetic to Spherical Equations: 17-18, WMM Technical report*/
    MAG_TimelyModifyMagneticModel(UserDate, MagneticModels[0], TimedMagneticModel); /* Time adjust the coefficients, Equation 19, WMM Technical report */
    MAG_Geomag(Ellip, CoordSpherical, CoordGeodetic, TimedMagneticModel, &GeoMagneticElements); /* Computes the geoMagnetic field elements and their time change*/
    MAG_CalculateGridVariation(CoordGeodetic, &GeoMagneticElements);
    MAG_WMMErrorCalc(GeoMagneticElements.H, &Errors);
    
    // Hushed for Python use
     //MAG_PrintUserDataWithUncertainty(GeoMagneticElements, Errors, CoordGeodetic, UserDate, TimedMagneticModel, &Geoid); /* Print the results */


    MAG_FreeMagneticModelMemory(TimedMagneticModel);
    MAG_FreeMagneticModelMemory(MagneticModels[0]);
    
    *X = GeoMagneticElements.X;
    *Y = GeoMagneticElements.Y;
    *Z = GeoMagneticElements.Z;
    *F = GeoMagneticElements.F;
    *Decl = GeoMagneticElements.Decl;
    *Incl = GeoMagneticElements.Incl;

    return EXIT_SUCCESS;
}
