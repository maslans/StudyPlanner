# Aplikacja Django

Aplikacja napisana we frameworku **Django**.

## Funkcjonalności aplikacji

- **Rejestracja** i **logowanie** użytkowników
- **Panel administracyjny** do zarządzania danymi w aplikacji.
- **Tworzenie** i **zarządzanie zadaniami, testami i egzaminami**
- **Importowanie** i **eksportowanie danych**
- **Chat** dla użytkowników z jednej uczelni
- **Przyjazny interfejs**
- **Zmiana danych użytkownika**
- **Wyświetlanie najbliższych terminów zadań, testów i egzmainów**
- **Oznaczenie zadania jako wykonane**
- **Dodawanie przedmiotów do globalnej bazy** oraz **przypisywanie ich pod konkretne zadania, testy, egzaminy**

##

## Testy obejmują 
- **Testy rejestracji**
    1. weryfikacja tworzenia usera
    2. weryfikacja tworzenia studenprofile
    3. weryfiakcja braku wymaganego pola "email"
    4. weryfikacja czy formularz zgłasza błedy
    5. weryfikacja poprawności wprowadzonego email bez "@"
    6. weryfikacja duplikacji "username"
- **Testy logowania**
    1. weryfikacja przekierownia po wprowadzeniu poprawnych danych na formularzu
    2. weryfikacja wyświetlania komunikatu w przypadku nieporawnej nazwy użytkownia lub hasła
    3. werfyiackaj braku uzupełnionych pól
    4. weryfikacja czy zalogowany użytkownik jest przekierowywany na stronę główną, gdy próbuje ponownie uzyskać dostęp do strony logowania.
- **Testy dodawania tasków**
    1. weryfikacja możliwości dodawania tasków dla zalogowanych użytkowników 
    2. weryfikacja daty
##