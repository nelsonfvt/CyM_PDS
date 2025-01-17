#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main()
{
    int N = 20;
    double mu = 0.0001;
    double xn[20] = {0};
    double hn[20] = {0.01};

    fstream fin;

    fin.open("samples_1.csv", ios::in);
    string num;

    double y = 0;
    double d = 0.05;

    while (getline(fin,num))
    {
        double e = d - y;
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
        cout << e << endl;
    }
    
}