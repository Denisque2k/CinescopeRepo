from sqlalchemy.orm import Session
import pytest
from annotations_practice.annotations_practice import user
from conftest import session
from db_models.transaction_template import AccountTransactionTemplate
from random import randint

def test_account_transaction_template(db_session: Session):
    stan = AccountTransactionTemplate(user=f"Stan_{randint(0, 10)}", balance=1000)
    bob = AccountTransactionTemplate(user=f"Bob_{randint(0, 10)}", balance=500)

    # Добавляем записи в сессию
    db_session.add_all([stan, bob])
    # Фиксируем изменения в базе данных
    db_session.commit()

    def transfer_money(session, from_account, to_account, amount):
        # пример функции выполняющей транзакцию
        # представим что она написана на стороне тестируемого сервиса
        # и вызывая метод transfer_money, мы какбудтобы делем запрос в api_manager.movies_api.transfer_money
        """
        Переводит деньги с одного счета на другой.
        :param session: Сессия SQLAlchemy.
        :param from_account: ID счета, с которого списываются деньги.
        :param to_account: ID счета, на который зачисляются деньги.
        :param amount: Сумма перевода.
        """
        # Получаем счета
        from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account).one()
        to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account).one()

        # Проверяем, что на счете достаточно средств
        if from_account.balance < amount:
            raise ValueError("Недостаточно средств на счете")

        # Выполняем перевод
        from_account.balance -= amount
        to_account.balance += amount

        # Сохраняем изменения
        session.commit()

    # ====================================================================== Тест
    # Проверяем начальные балансы
    assert stan.balance == 1000
    assert bob.balance == 500

    try:
        # Выполняем перевод 200 единиц от stan к bob
        transfer_money(db_session, from_account=stan.user, to_account=bob.user, amount=1200)

        # Проверяем, что балансы изменились
        assert stan.balance == 800
        assert bob.balance == 700

    except Exception as e:
        # Если произошла ошибка, откатываем транзакцию
        db_session.rollback()  # откат всех введеных нами изменений
        pytest.fail(f"Ошибка при переводе денег: {e}! Баланс {stan.user} = {stan.balance}, баланс {bob.user} = {bob.balance}")

    finally:
        # Удаляем данные для тестирования из базы
        db_session.delete(stan)
        db_session.delete(bob)
        # Фиксируем изменения в базе данных
        db_session.commit()