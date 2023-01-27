function [X,mu,Sigma,err] = bug_demo()
%Simulate the EKF on a problem of a bug movement estimation with
%Estimate x and y position based on prior state

%set up and display simulation parameters

 X = gen_sim_data();
 Z = get_obs(X);

 %Initial given distribution

 [mu{1}, Sigma{1}, Sigma_x] = initial_distribution(Z);
 err = mu{1}-X{1};
 err = norm(err(1:2));

 for T = 2:size(Z,2)
   muprev = mu{T-1};
   [pred_x,Jf] = sysf(muprev);
   [pred_z,H,Sigma_z] = sysh(pred_x);
   pred_sig = Jf*Sigma{T-1}*Jf' + Sigma_x;
   residual = Z{T}-pred_z;
   e(T) = norm(residual);
   K = pred_sig * H' * inv( H * pred_sig * H' + Sigma_z );
   Sigma{T} = (eye(size(K,1)) - K * H) * pred_sig;
   munew = pred_x + K * residual;
   mu{T} = munew;
   xnew = X{T};
   err(T) = norm(munew(1:3) - xnew(1:3));
 end

 figure(1);
 plot_sim_data(X, Z, mu);

end

function X = gen_sim_data()

 X{1} = [0.1 45 1.6667]';% [dl theta_l v]
 %The object takes about 1minute to travel along a stright line in XY plane
 %getting 100 cm of distance.
 t = 1;

 for i=1:50
     t = t+1;
     prevX = X{t-1};    %Last state
     dl    = prevX(1);  %Last left lateral distance
     theta_l = prevX(2);  %Last angle of the bug to left side of sink
     v     = prevX(3);  %Last velocity
     delta_t = 1/30;
     d = v*delta_t;     

 %Distance, delta_t at 30s

 %Velocity 100cm/min

     ll = d*cos(theta_l*pi/180);
     New_dl = dl+ll;
     newX = [New_dl theta_l v]';
     X{t} = newX;

 end

end

function Z = get_obs(X)

  for i = 1:size(X,2)
      thisx = X{i};
      obs_dl = thisx(1)+(randn(1)/5);
      Z{i} = [obs_dl]';
  end

end

function  [mu, Sigma, Sigma_x] = initial_distribution(Z)

  thisz = Z{1};
  mu = [thisz(1) 0  0]';
  Sigma = diag([0.1 10/180*pi 0.5].^2);
  deltat = 1/30;
  Sigma_x = diag((deltat*[0.1 10/180*pi 0.5].^2));

end

% System model and Jacobian 

function [xnew,J] = sysf(xold)

  dl      = xold(1);
  theta_l = xold(2);
  v       = xold(3);
  delta_t = 1/30;
  xnew = [dl+(delta_t*v*cos(theta_l))
            theta_l
            v];

  %Jacobian

  grad_dlnew = [1, (delta_t*v*- sin(theta_l)), (delta_t*cos(theta_l))];

  J = [grad_dlnew
       0 1 0 
       0 0 1];

end

% measurement model

function [Z,H,Sigma_z] = sysh(X)

  H = [1 0 0];
  Z = H*X;
  Sigma_z = [0.05];

end

 

% visualization

function plot_sim_data(X, Z, Xest)

  %plot of dl

  subplot(1,1,1);

  for i = 1:size(X,2)
      thisx = X{i};
      plotx(i) = thisx(1);
  end

  hold off;
  plot(plotx,' -.*r');
  hold on;
  for i = 1:size(X,2)
      thisx = Z{i};
      plotx(i) = thisx(1);
  end

  plot(plotx, '-.og');

  if ~isempty(Xest)

      for i = 1:size(X,2)
          thisx = Xest{i};
          plotx(i) = thisx(1);
      end
      plot(plotx,'-.+b');

  end

  hold off;
  title 'estimation of d_l';

end