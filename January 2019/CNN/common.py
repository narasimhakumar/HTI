

#general structure

GRDim =		'_rlnReferenceDimensionality'
GDDim =		'_rlnDataDimensionality'
GOImg =		'_rlnOriginalImageSize'
GCRes =		'_rlnCurrentResolution'
GCImg =		'_rlnCurrentImageSize'
GPF = 		'_rlnPaddingFactor'
GIH = 		'_rlnIsHelix'
GFSI = 		'_rlnFourierSpaceInterpolator'
GMRI = 		'_rlnMinRadiusNnInterpolation'
GPSz = 		'_rlnPixelSize'
GNrC = 		'_rlnNrClasses'
GNrB = 		'_rlnNrBodies'
GNrG = 		'_rlnNrGroups'
GT2FF = 	'_rlnTau2FudgeFactor'
GNCA = 		'_rlnNormCorrectionAverage'
GSO = 		'_rlnSigmaOffsets'
GOPM = 		'_rlnOrientationalPriorMode'
GSPRA = 	'_rlnSigmaPriorRotAngle'
GSPTA = 	'_rlnSigmaPriorTiltAngle'
GSPPA = 	'_rlnSigmaPriorPsiAngle'
GLH = 		'_rlnLog`hood'
GAP = 		'_rlnAveragePmax'

#classes structure

CRImg =		'_rlnReferenceImage'
CCD =		'_rlnClassDistribution'
CAR = 		'_rlnAccuracyRotations'
CAT = 		'_rlnAccuracyTranslations'
CER = 		'_rlnEstimatedResolution'
COFC =	 	'_rlnOverallFourierCompleteness'
CCPOX = 	'_rlnClassPriorOffsetX'
CCPOY =		'_rlnClassPriorOffsetY'

dmg_labels = 		[GRDim, GDDim, GOImg,GCRes, GCImg, GPF, GIH, GFSI, GMRI, \
			 		 GPSz, GNrC, GNrB, GNrG, GT2FF, GNCA, GSO, GOPM, GSPRA, GSPTA, GSPPA, GLH, GAP]
dmc_labels = 		[CRImg, CCD, CAR, CAT, CER, COFC, CCPOX, CCPOY]
sdmc_labels = 		[CRImg, CCD, CAR, CAT, CCPOX, CCPOY]

summary_labels = 	[
#					GRDim, GDDim, GOImg, \
#					GCRes, \
#					GCImg, GPF, GIH, GFSI, GMRI, \
					GPSz, \
#					GNrC, GNrB, GNrG, GT2FF, \
#					GNCA, GSO, \
#					GOPM, GSPRA, GSPTA, GSPPA, \
#					GLH, GAP, \
					CCD, CAR, CAT, \
#					CER, COFC, \
					CCPOX, CCPOY]


