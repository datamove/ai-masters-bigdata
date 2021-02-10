from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, GridSearchCV

#
# Dataset fields
#
fields = """doc_id,hotel_name,hotel_url,street,city,state,country,zip,class,price,
num_reviews,CLEANLINESS,ROOM,SERVICE,LOCATION,VALUE,COMFORT,overall_ratingsource""".replace("\n",'').split(",")

#
# Model pipeline
#

# We create the preprocessing pipelines for both numeric and categorical data.
numeric_features = ['CLEANLINESS', 'ROOM', 'SERVICE', 'LOCATION']
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
#    ('scaler', StandardScaler())
])

categorical_features = ['city', 'country']
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

# Now we have a full prediction pipeline.
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('linearregression', LinearRegression())
])

