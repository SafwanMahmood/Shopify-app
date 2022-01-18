class Validate:
    
    def validate_product(self,product_id,name,price,available_count):
        if not isinstance(product_id,(int)):
            return ValueError("Product Id: Int expected")
        if not isinstance(name,(str)):
            return ValueError("Name: Str/text expected")    
        if not isinstance(price,(int,float)):
            return ValueError("Price: Int/float expected")
        if not isinstance(available_count,(int)):
            return ValueError("Availablity Count: Int expected")
        return True