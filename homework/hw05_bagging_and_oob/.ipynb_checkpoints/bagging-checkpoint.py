import numpy as np



class SimplifiedBaggingRegressor:
    def __init__(self, num_bags, oob=False):
        self.num_bags = num_bags
        self.oob = oob
        
    def _generate_splits(self, data: np.ndarray):
        '''
        Generate indices for every bag and store in self.indices_list list
        '''
        self.indices_list = []
        data_length = len(data)
        for _ in range(self.num_bags):
            self.indices_list.append(np.random.randint(0, data_length, data_length))
            
        
    def fit(self, model_constructor, data, target):
        '''
        Fit model on every bag.
        Model constructor with no parameters (and with no ()) is passed to this function.
        
        example:
        
        bagging_regressor = SimplifiedBaggingRegressor(num_bags=10, oob=True)
        bagging_regressor.fit(LinearRegression, X, y)
        '''
        self.data = None
        self.target = None
        self._generate_splits(data)
        assert len(set(list(map(len, self.indices_list)))) == 1, 'All bags should be of the same length!'
        assert list(map(len, self.indices_list))[0] == len(data), 'All bags should contain `len(data)` number of elements!'
        self.models_list = []
        for bag in range(self.num_bags):
            model = model_constructor()
            data_bag = data[self.indices_list[bag]]
            target_bag = target[self.indices_list[bag]]
            self.models_list.append(model.fit(data_bag, target_bag)) # store fitted models here
        if self.oob:
            self.data = data
            self.target = target
        
    def predict(self, data):
        '''
        Get average prediction for every object from passed dataset
        '''
        predistions = []
        for model in self.models_list:
            predistions.append(model.predict(data))
        return predistions
    
    def _get_oob_predictions_from_every_model(self):
        '''
        Generates list of lists, where list i contains predictions for self.data[i] object
        from all models, which have not seen this object during training phase
        '''
        list_of_predictions_lists = []
        for i in range(len(self.data)):
            arr = []
            idx_models_list = np.array([i not in tmp for tmp in self.indices_list])
            for model in np.array(self.models_list)[idx_models_list]:
                arr.append(model.predict(self.data[i].reshape(1, -1)).item())
            list_of_predictions_lists.append(arr)
        self.list_of_predictions_lists = np.array(list_of_predictions_lists, dtype=object)
    
    def _get_averaged_oob_predictions(self):
        '''
        Compute average prediction for every object from training set.
        If object has been used in all bags on training phase, return None instead of prediction
        '''
        self._get_oob_predictions_from_every_model()
        oob_tmp = []
        for curr in self.list_of_predictions_lists:
            if len(curr) > 0:
                oob_tmp.append(np.mean(curr))
            else:
                oob_tmp.append(None)
        self.oob_predictions = oob_tmp
        
        
    def OOB_score(self):
        '''
        Compute mean square error for all objects, which have at least one prediction
        '''
        self._get_averaged_oob_predictions()
        result_score = []
        for curr_oob, curr_target in zip(self.oob_predictions, self.target):
            if curr_oob is None:
                continue
            result_score.append(np.power(curr_oob - curr_target, 2))
        return np.mean(result_score)