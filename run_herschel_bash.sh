#!/bin/bash
# -*- coding: utf-8 -*-

#####################################################
#
# EXAMPLE SCRIPT FILE TO PRODUCE A BATCH OF KERNELS
#
# This file produces kernels
#   from PACS 70 and 160 and SPIRE 250 and 350 microns
#   to SPIRE 500 microns
#   for OrionBar and HorseHead obs
#   at temperatures between 15 and 90 degrees
#   spectral index between 10 and 25#
#
# Alexandre Boucaud <alexandre.boucaud@ias.u-psud.fr>
# Date: 20/02/2015
#####################################################

# If case of error during execution, exit the script
set -e

# Regularization factor
# TO BE CHANGED according to provided data.
regfact=0.0001

# Path
#------
# TO BE CHANGED according to your directory structure
CODEPATH=$HOME/work/devel/homogenization/trunk
DATAPATH=$HOME/work/Herschel/simulations/
OUTPATH=$DATAPATH/kernels

# Create directory if it does not exist
mkdir -p $OUTPATH

# Lists
#-------
# The following purely depends on the filenames and must be changed according so.
names=(
    OrionBar
    HorseHead
)

temperature=(
    15
    20
    25
    30
    35
    40
    45
    50
    55
    60
    65
    70
    75
    80
    85
    90
)

betas=(
    10
    15
    20
    25
)


# Main
#------
echo "-------------------------------"
echo "Starting make_psf_kernel script"
echo "-------------------------------"
echo ""

# Position loop
# -------------
for name in ${names[@]}; do

    case $name in
        'OrionBar' ) angle_pacs=258.45839 ;;
        'HorseHead' ) angle_pacs=73.638783 ;;
    esac

    case $name in
        'OrionBar' ) angle_spire=15.825038 ;;
        'HorseHead' ) angle_spire=15.849217 ;;
    esac

    # Temperature loop
    # ----------------
    for temp in ${temperature[@]}; do

        # Beta loop
        #----------
        for beta in ${betas[@]}; do

            psf_target=PSF_PLW_temp${temp}beta${beta}_Alain.fits
            angle_target=$angle_spire

            # Band loop
            # ---------
            for band_input in blue red PSW PMW; do

                psf_input=PSF_${band_input}_temp${temp}beta${beta}_Alain.fits

                case $band_input in
                    'red' ) angle_input=$angle_pacs ;;
                    'blue') angle_input=$angle_pacs ;;
                    'PSW' ) angle_input=$angle_spire ;;
                    'PMW' ) angle_input=$angle_spire ;;
                esac

                # Create homogenization kernel
                echo "Computing kernel from $band_input to PLW"

                kernel=${name}_temp${temp}beta${beta}_kernel_${band_input}_to_PLW.fits

                $CODEPATH/make_psf_kernel -v \
                    $DATAPATH/${psf_input} \
                    $DATAPATH/${psf_target} \
                    $OUTPATH/${kernel} \
                    -r ${regfact} \
                    --angle_input ${angle_input} \
                    --angle_target ${angle_target}

                echo "Kernel stored as $OUTPATH/${kernel}"

            done
        done
    done
done
