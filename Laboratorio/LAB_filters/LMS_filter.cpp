#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main()
{
    int N = 20;
    double mu = 0.001;
    double xn[20] = {0};
    double hn[20] = {0.01};

    fstream fin;

    fin.open("samples_1.csv", ios::in);
    string num;

    double y = 0;
    double e = 0;

    while (getline(fin,num))
    {
        double d = -0.3*stod(num) + 0.125*xn[0] -0.1*xn[1] + 0.5*xn[2]; //algo simple
        y = 0;
        for(int i = N-1; i > 0; i--)
        {
            xn[i] = xn[i-1];
            y += xn[i] * hn[i];
            hn[i] += mu*e*xn[i];
        }
        xn[0] = stod(num);
        y += xn[0] * hn[0];
        hn[0] += mu*e*xn[0];
        e = d - y;
        cout << " d: " << d << " y: " << y << " e: " << e << endl;
    }
}