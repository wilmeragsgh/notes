# lpSolve Library

## Recipes

**Load balancing R example**

```R
install.packages('lpSolve')
library('lpSolve')

## Set the coefficients of the decision variables -> C
capacities.leads <- c(170,165,120,140,175,165,140,105,55)
capacities.positions <- ceiling(capacities.leads / 10)
coeff <- (capacities.positions ** -1) * (length(capacities.leads)**-1)
n.teams <- length(capacities.positions)
# Create constraint martix B
A <- matrix(c(diag(n.teams) * (capacities.positions**-1 ),
         diag(n.teams) * (capacities.positions**-1),
         rep(1,n.teams)),ncol = n.teams,byrow = T)

# Right hand side for the constraints
B <- c(rep(0.82,n.teams),
       rep(0.92,n.teams),
       110
)

# Direction of the constraints
constranints_direction  <- c(rep(">",n.teams),
                             rep("<",n.teams),
                             "==")

# Find the optimal solution
optimum <-  lp(direction="min",
               objective.in = coeff,
               const.mat = A,
               const.dir = constranints_direction,
               const.rhs = B,
               all.int = T)

# Print status: 0 = success, 2 = no feasible solution
print(optimum$status)

# Display the optimum values for x_4p, x_3p and x_w
best_sol <- optimum$solution
names(best_sol) <- c("Augusto","Alexander","Josmayry","Carlina","Gabriela","Maria Carolina","Tiziana","Gustavo","Jhem") 
print(best_sol)

# Check the value of objective function at optimal point
print(paste("Total cost: ", optimum$objval, sep=""))
```

