class DataProcessor:
    @staticmethod
    def filter_outliers(datos):
        if not datos:
            return []
        mean = sum([d['value'] for d in datos]) / len(datos)
        varianza = sum((d['value'] - mean) ** 2 for d in datos) / (len(datos) - 1)
        std = varianza ** 0.5
        low = mean - 3 * std
        high = mean + 3 * std
        return [d for d in datos if low <= d['value'] <= high]
