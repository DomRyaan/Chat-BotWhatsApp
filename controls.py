

class BusinessRules:
    """ Classe para gerenciar Regras de Negócio """
    def __init__(self, morning_start: int = 6, morning_end: int = 11, evening_start: int = 14, evening_end: int = 18):
        """
        Inicializa os horarios de Funcionamento.

        :param morning_start: Hora que o estabelecimento abre no periodo da manhã.
        :param morning_end: Hora que o estabelicmento fecha no periodo da manhã.
        :param evening_start: Hora que o estabelecimento abre no periodo da tarde.
        :param evening_end: Hora que o estabelecimento fecha no periodo da tarde.
        """
        self.morning_start = morning_start
        self.morning_end = morning_end
        self.evening_start = evening_start
        self.evening_end = evening_end    


    def is_open(self, hour: int) -> bool:
        """
        Verifica se o horário está dentro do período de funcionamento.

        :param hour: Hora atual (formato 24h).
        :return: True se estiver dentro do horário de funcionamento, False caso contrário.
        """
        return self.morning_start <= hour < self.morning_end or self.evening_start <= hour < self.evening_end