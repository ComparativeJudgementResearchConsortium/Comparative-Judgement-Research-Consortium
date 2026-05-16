library(speedyBBT)

# Load the data
data <- read.csv("CJRC2026_RAVE.csv")

# Get unique items and map to integer IDs
items <- unique(c(data$choice_id1, data$choice_id2))
n.objects <- length(items)
item_lookup <- setNames(seq_along(items), items)

# Map choice IDs to integer indices
player1 <- item_lookup[as.character(data$choice_id1)]
player2 <- item_lookup[as.character(data$choice_id2)]

# Outcome: 0 if player1 (choice_id1) wins, 1 if player2 (choice_id2) wins
outcome <- ifelse(data$winner_id == data$choice_id2, 0, 1)

# Fit the BT model on the full dataset
cat("Fitting BT model on full dataset...\n")
full_model <- speedyBBTm(outcome = outcome,
                         player1 = player1,
                         player2 = player2,
                         player.prior.var = 20*diag(n.objects), 
                         hyperparameter = FALSE,
                         n.iter = 5000)

# Posterior summaries (discarding first 1000 as burn-in)
lambda_samples <- full_model$lambda[1001:5000, ]
lambda_median <- apply(lambda_samples, 2, median)
lambda_lower <- apply(lambda_samples, 2, quantile, probs = 0.025)
lambda_upper <- apply(lambda_samples, 2, quantile, probs = 0.975)
names(lambda_median) <- items
names(lambda_lower) <- items
names(lambda_upper) <- items

# Build lookup from item ID to question text
item_text <- c(setNames(data$choice1_text, data$choice_id1),
               setNames(data$choice2_text, data$choice_id2))
item_text <- item_text[!duplicated(names(item_text))]

# Show top 10 questions
top10 <- sort(lambda_median, decreasing = TRUE)[1:10]
cat("\n--- Top 10 Questions ---\n")
for (i in seq_along(top10)) {
  cat(sprintf("%2d. [Score: %6.3f] %s\n", i, top10[i],
              substr(item_text[names(top10)[i]], 1, 120)))
}
cat("\n")

# Plot posterior medians with 95% CIs ordered
rank_order <- order(lambda_median)
plot(1:n.objects, lambda_median[rank_order],
     ylim = range(c(lambda_lower, lambda_upper)),
     xlab = "Rank", ylab = "Quality estimate",
     main = "Posterior medians with 95% credible intervals",
     pch = 19, cex = 0.6, col = "steelblue")
arrows(1:n.objects, lambda_lower[rank_order],
       1:n.objects, lambda_upper[rank_order],
       length = 0, col = "steelblue", lwd = 0.8)
abline(h = 0, lty = 2, col = "grey50")

# --- Split halves analysis (200 random splits of judges) ---
judges <- unique(data$participant_id)
n_judges <- length(judges)
n_splits <- 200

correlations <- numeric(n_splits)

set.seed(42)
cat("Running split halves analysis (200 iterations)...\n")

for (iter in 1:n_splits) {
  # Randomly allocate judges to two halves
  shuffled <- sample(judges)
  half1_judges <- shuffled[1:floor(n_judges / 2)]
  half2_judges <- shuffled[(floor(n_judges / 2) + 1):n_judges]

  half1_idx <- which(data$participant_id %in% half1_judges)
  half2_idx <- which(data$participant_id %in% half2_judges)

  # Fit model on first half
  model_half1 <- speedyBBTm(outcome = outcome[half1_idx],
                            player1 = player1[half1_idx],
                            player2 = player2[half1_idx],
                            player.prior.var = 20 * diag(n.objects),
                            hyperparameter = FALSE,
                            n.iter = 5000)

  # Fit model on second half
  model_half2 <- speedyBBTm(outcome = outcome[half2_idx],
                            player1 = player1[half2_idx],
                            player2 = player2[half2_idx],
                            player.prior.var = 20 * diag(n.objects),
                            hyperparameter = FALSE,
                            n.iter = 5000)

  # Posterior means for each half
  lambda_half1 <- colMeans(model_half1$lambda[1001:5000, ])
  lambda_half2 <- colMeans(model_half2$lambda[1001:5000, ])

  correlations[iter] <- cor(lambda_half1, lambda_half2)

  cat(sprintf("  Iteration %d/%d: r = %.4f\n",
              iter, n_splits, correlations[iter]))
}

# Summary
cat("\n--- Split Halves Summary (200 random splits) ---\n")
cat(sprintf("Mean correlation:            %.4f (SD = %.4f)\n", mean(correlations), sd(correlations)))
cat(sprintf("Range of correlations:       [%.4f, %.4f]\n", min(correlations), max(correlations)))

# Plot distribution of correlations
hist(correlations, breaks = 20, col = "steelblue",
     main = "Split halves  reliability (200 random splits)",
     xlab = "Split halves correlation")
abline(v = mean(correlations), col = "red", lwd = 2, lty = 2)
