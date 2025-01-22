#include <iostream>
#include <fstream>
#include <string>
#include <cmath>

using namespace std;

double dot_p(double* , double*, int);
double* mat_vec(double**, double*, int);
double** mat_mat(double**, double**, int);
double** vec_vec(double*, double*, int);
double* get_g(double**, double*, double, int);
void upd_P(double**, double*, double*, double, int);

int main()
{
    int N = 20;
    double lam = 1;
    double xn[20] = {0};
    double hn[20] = {0.01};
    double** P = new double*[N];
    for(int i=0; i<N; i++)
    {
        P[i] = new double[N];
        P[i][i] = 0.8;
    }

    double y = 0;
    double e = 0;

    fstream fin;

    fin.open("samples_1.csv", ios::in);
    string num;

    while (getline(fin,num))
    {
        double ndato = stod(num);
        double d = -0.3*ndato + 0.125*xn[0] -0.1*xn[1] + 0.5*xn[2]; //algo simple

        y = 0;
        for(int i=N-1; i>0; i--)
        {
            xn[i] = xn[i-1];
            y += xn[i] * hn[i];
        }
        xn[0] = ndato;
        y += xn[0] * hn[0];

        e = d-y;
        double* g = get_g(P, xn, lam, N);

        for(int i=0; i<N; i++)
        {
            hn[i] += g[i] * e;
        }

        upd_P(P,g,xn,lam,N);

        cout << " d: " << d << " y: " << y << " e: " << e << endl;
        
        delete[] g;
    }
}

// Operaciones filtro

double* get_g(double** P, double* x, double l, int N)
{
    double* Px = mat_vec(P,x,N);
    double lxPx = l + dot_p(x, Px, N);

    double* res = new double[N];
    for(int i = 0; i<N; i++)
    {
        res[i] = Px[i]/lxPx;
    }
    delete[] Px;
    return res;
}

void upd_P(double** P, double* g, double* x, double l, int N)
{
    
    double** gxP = mat_mat( vec_vec(g,x,N), P, N);

    for(int i = 0; i<N; i++)
    {
        for(int j=0; j<N; j++)
        {
            P[i][j] = (P[i][j] - gxP[i][j])/l;
            
        }
        delete[] gxP[i];
    }
    delete[] gxP;
}

// Algebra lineal

double dot_p(double* v1, double* v2, int size)
{
    double dp = 0;
    for(int i=0; i<size; i++)
    {
        dp += v1[i] * v2[i];
    }
    return dp;
}

double* mat_vec(double** Mx, double* v, int size)
{
    double* res = new double[size];
    
    for(int i = 0; i<size; i++)
    {
        res[i] = 0;
        for(int j=0; j<size; j++)
        {
            res[i] += Mx[i][j] * v[j];
        }
    }
    
    return res;
}

double** mat_mat(double** M1, double** M2, int size)
{
    double** res = new double*[size];
    for(int i=0; i<size; i++)
    {
        res[i] = new double[size];
        for(int j=0;j<size;j++)
        {
            res[i][j] = 0;
            for(int k=0; k<size; k++)
            {
                res[i][j] += M1[i][k] * M2[k][j];
            }
        }

    }
    return res;
}

double** vec_vec(double* v1, double* v2, int size)
{
    double** res = new double*[size];
    for(int i=0; i<size; i++)
    {
        res[i] = new double[size];
        for( int j=0; j<size; j++)
        {
            res[i][j] = v1[i] * v2[j];
        }
    }

    return res;
}