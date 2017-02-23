%This checks if a non default simulink library is present.  This library is
%required for our simulation.  It is provided by the MathWorks from their
%site.  As I am not sure if we can include it in our
%repository/distribution, this script serves to aid in its installation.

NOT_FOUND       = 0;
FOUND_SIMULINK  = 4;
URL             = '<a href="http://www.mathworks.com/matlabcentral/fileexchange/37636-simscape-multibody-3d---1d-interface-examples">Simscape Multibody 3D – 1D Interface Examples</a>\n';
LIB_NAME        = 'multibody_3D_1D_intf_lib';

test = exist(LIB_NAME);
%test = 3;
if test == NOT_FOUND
    fprintf(strcat('Library not found. Proceed to:\n ', URL))
    fprintf('Attempting to add library to MATLAB path.')
    cd 'Multibody Interfaces'
    addpath(pwd)
elseif test == FOUND_SIMULINK
    fprintf('Library is found.\n')
else
    fprintf(strcat('Unrecognized result for exist command: ',num2str(test),'\n'))
    fprintf('See documentation for exist command.')
    doc exist
end