# Минипроект взаимодействия DJANGO c системой STRIPE

## Описание

Через админ-панель можно создать товар, купон, заказ и список заказанных товаров. Далее по адресу '/order/{номер заказа}' будет видно список закзанных позиций, наличие или отсутствие скидки и итоговую цену, на этой же странице есть кнопка 'оплатить', после нажатия на которую происходит переход на тестовую checkout-страницу STRIPE с возможностью оплаты.

В проекте реализована возможность оплаты товара в долларах и евро, зависит от выбранной валюты корзины, а также возможность применения скидки к конкретному заказу, которая создается так же через админ-панель.

Проект возводится полностью в Docker-е, используется следующий стек: Stripe, PostgreSQL и т.д.

## Установка и запуск в тестовом формате:

- docker-compose up
