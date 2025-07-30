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
