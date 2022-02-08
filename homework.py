"""Fitness tracker module ver.1.0.4 alpha"""

from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: int
    pass

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000

    action: int
    duration: float
    weight: float

    def get_spent_calories(self):
        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        dist = self.action * self.LEN_STEP / self.M_IN_KM
        return dist

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_type = self.__class__.__name__
        distance_info = self.get_distance()
        speed_info = self.get_mean_speed()
        calories_info = self.get_spent_calories()
        msg = InfoMessage(
            training_type, self.duration,
            distance_info, speed_info, calories_info)
        return msg


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self):
        speed_ave = self.get_mean_speed()
        COEFF_CAL_1 = 18
        COEFF_CAL_2 = 20
        min_in_hour = 60
        count_calories = (
            (COEFF_CAL_1 * speed_ave - COEFF_CAL_2)
            * self.weight / self.M_IN_KM * self.duration * min_in_hour)
        return count_calories


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: int

    def get_spent_calories(self):
        speed_ave = self.get_mean_speed()
        COEFF_CAL_1 = 0.035
        COEFF_CAL_2 = 0.029
        min_in_hour = 60
        count_calories = (
            (COEFF_CAL_1 * self.weight
             + (speed_ave**2 // self.height)
             * COEFF_CAL_2 * self.weight)
            * self.duration * min_in_hour)
        return count_calories


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38

    length_pool: int
    count_pool: int

    def get_mean_speed(self):
        speed_ave = (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration)
        return speed_ave

    def get_spent_calories(self):
        speed_ave = self.get_mean_speed()
        COEFF_CAL_1 = 1.1
        COEFF_CAL_2 = 2
        count_calories = (
            (speed_ave + COEFF_CAL_1)
            * COEFF_CAL_2 * self.weight)
        return count_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    dict_of_actions = {'SWM': Swimming,
                       'RUN': Running,
                       'WLK': SportsWalking}
    try:
        if workout_type in dict_of_actions:
            i = dict_of_actions[workout_type](*data)
            return i
    except Exception:
        print('Error')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    msg = info.get_message()
    print(msg)
    return


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
