# Минипроект взаимодействия DJANGO c системой STRIPE

## Описание

Через админ-панель можно создать товар, купон, корзину и список заказанных товаров. По адресу '/items/all' отображается список всех товаров на сервисе, которых можно добавить в себе в корзину. Далее по адресу '/order/{номер корзины}' будет видно список закзанных позиций, наличие или отсутствие скидки и итоговую цену, на этой же странице есть кнопка 'оплатить', после нажатия на которую происходит переход на тестовую checkout-страницу STRIPE с возможностью тестовой оплаты.

В проекте реализована возможность оплаты товара в долларах и евро, зависит от выбранной валюты корзины, а также возможность применения скидки к конкретному заказу, которая создается так же через админ-панель.

Проект возводится полностью в Docker-е, используется следующий стек: Stripe, PostgreSQL и т.д.

## Установка и запуск в тестовом формате:

- docker-compose up

P.S. Это проект является своего рода шаблоном/заготовкой к более крупному сервису, так как в него изначально заложена возможность функционального расширения при желании.
