# Data Preprocessing

In here we do some data preprocessing in data mining practices.

### Slide 7: Errors in Data

**Simple remedy:**
- Remove data points outside a given interval  
  *(requires domain knowledge)*
  - Example:  
    - Remove temperature values outside -30 to +50 °C  
    - Remove negative durations  
    - Remove purchases above 1M Euro  

**Advanced remedy:**
- Automatically find suspicious data points using **Anomaly Detection**

---

### Slide 8: Missing Values

**Possible reasons:**
- Sensor failure  
- Data loss  
- Information not collected  
- Customers skipped fields like age, sex, marital status  
- ...

---

### Slide 9: Missing Values – Treatments

**Treatment options:**
- Ignore records with missing values in training data  
- Replace missing value with:
  - Default/special value (e.g., `0`, `"missing"`)
  - Mean or median for numeric attributes  
  - Most frequent value for nominal attributes  
  - `SimpleImputer(missing_values=np.nan, strategy='mean')`
- Predict missing values:
  - Treat missingness as a learning problem  
  - Use observed data to train, and predict missing values  
  - Example: `KNNImputer(n_neighbors=2, weights="uniform")`

[SimpleImputer Docs](https://scikit-learn.org/1.5/modules/generated/sklearn.impute.SimpleImputer.html)  
[KNNImputer Docs](https://scikit-learn.org/1.5/modules/generated/sklearn.impute.KNNImputer.html)


### Slide 10: Missing Values – Important Note

Not all missing values are the same.  
Some are **random**, others are **not random**.

**Examples (not random):**
- Optional survey questions (e.g., "How often do you drink alcohol?")
- Data only collected in special cases (e.g., university grade if graduated)
- Values valid for specific groups (e.g., "Are you sick?")
- Sensors that fail under certain conditions (e.g., high temperature)

👉 Be careful: **"missing" can carry important meaning!**

### Slide 11: Handling Missing Values – Example Problem

Imagine a medical trial studying side effects of a drug.  
- Only 50 people have their blood sugar recorded.
- Out of those 50, **40 have high blood sugar**, and **30 of them got side effects**.

**Observation:**
- People with high blood sugar → 75% chance of side effects  
- Overall side effect rate → ~23%

Now you know: missing values **can hide patterns**.

---

### Slide 12: Handling Missing Values – Danger of Imputation

If we fill in missing blood sugar values with the most common value ("yes"):
- The number of "high blood sugar" people becomes much higher.
- The pattern disappears: risk seems **lower**, not higher!

**Result:**
- Side effect risk seems **less** for people with high blood sugar.
- But that’s **wrong**, because we **filled in missing values blindly**.

👉 **Conclusion:** Imputing without thinking can destroy useful information!


### Slide 14: Resampling Unbalanced Data

Sometimes your dataset is **unbalanced** — one class has many more examples than the other.

**Example:**
- Class A: 1000 samples
- Class B: 10 samples

This makes it hard for a model to learn from the smaller class.

---

### Two Main Strategies

1. **Downsampling the larger class**  
   → Reduce Class A to 10 samples to match Class B  
   🔴 Problem: You throw away a lot of data!

2. **Upsampling the smaller class**  
   → Make many copies of Class B  
   🔴 Problem: Model might **just memorize** those few examples.

---

🎯 Goal:  
- Use **as much data** as possible  
- Keep the training set **diverse**

➡️ It’s a trade-off!

### Slide 15: Resampling Unbalanced Data – Continued

Let’s look again at a dataset:

- **Class A**: 1000 samples  
- **Class B**: 10 samples

---

**Downsampling:**
- Keep only 10 samples from Class A  
- 🔴 You lose 990 examples = less training data

**Upsampling:**
- Make 100 copies of each Class B sample  
- 🔴 The model might just memorize Class B and not learn anything general

---

💡 **Better solutions:**
- Use smarter techniques like **SMOTE** (covered in next slide)
- Use Python libraries:  
  [imbalanced-learn.org](https://imbalanced-learn.org/)
