#include <iostream>
#include <fstream>
#include <string>
#include <cmath>

using namespace std;

double dot_p(double* , double*, int);

int main()
{
    int N = 20;
    double mu = 0.1;
    double xn[20] = {0};
    double hn[20] = {0.01};

    fstream fin;

    fin.open("samples_1.csv", ios::in);
    string num;

    double y = 0;
    double e = 0;
    double Sx = 0;

    while (getline(fin,num))
    {
        double ndato = stod(num);
        double d = -0.3*ndato + 0.125*xn[0] -0.1*xn[1] + 0.5*xn[2]; //algo simple
        y = 0;
        Sx = dot_p(xn, xn, 20);
        if(Sx == 0)
            Sx = 0.0001;
        
        for(int i = N-1; i > 0; i--)
        {
            xn[i] = xn[i-1];
            y += xn[i] * hn[i];
            hn[i] = hn[i] + (mu*e*xn[i] / Sx);
        }
        xn[0] = ndato;
        y += xn[0] * hn[0];
        hn[0] = hn[0] + (mu*e*xn[0] / Sx);
        e = d - y;
        cout << " d: " << d << " y: " << y << " e: " << e << endl;
    }
    
}

double dot_p(double* v1, double* v2, int size)
{
    double dp = 0;
    for(int i=0; i<size; i++)
    {
        dp += v1[i] * v2[i];
    }
    return dp;
}