@echo off
setlocal enabledelayedexpansion

set "SRC_CRT=./TWCA Secure SSL Certification Authority_2023G3.crt"

set "OUT_PEM=./twca_intermediate.pem"

certutil -encode "%SRC_CRT%" "%OUT_PEM%"
