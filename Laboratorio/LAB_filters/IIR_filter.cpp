#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main()
{
    int N = 4;
    double xn[4] = {0};
    double yn[4] = {0};
    double num[4] = {0.0316893438497110,	0.0950680315491331,	0.0950680315491331,	0.0316893438497110};
    double den[4] = {1,	-1.45902906222806,	0.910369000290069,	-0.197825187264319};

    fstream fin;

    fin.open("samples_1.csv", ios::in);
    string val;

    while (getline(fin, val))
    {
        double y = 0;
        for(int i = N-1; i > 0; i--)
        {
            xn[i] = xn[i-1];
            yn[i] = yn[i-1];
            y += num[i] * xn[i] - den[i] * yn[i];
        }
        xn[0] = stod(val);
        y += num[0] * xn[0];
        yn[0] = y;
        
        cout << y << endl;
    }
    
}