import streamlit as st
import numpy as np

def least_cost_method(costs, supply, demand):
    rows, columns = len(supply), len(demand)
    filled_values = [[0 for _ in range(columns)] for _ in range(rows)]

    while sum(supply) > 0 and sum(demand) > 0:
        min_cost = float('inf')
        min_i, min_j = -1, -1
        for i in range(rows):
            for j in range(columns):
                if costs[i][j] < min_cost and supply[i] > 0 and demand[j] > 0:
                    min_cost = costs[i][j]
                    min_i, min_j = i, j

        if min_i == -1 or min_j == -1:
            raise ValueError("Impossible de trouver une cellule valide. Vérifiez les entrées.")

        quantity = min(supply[min_i], demand[min_j])
        filled_values[min_i][min_j] = quantity
        supply[min_i] -= quantity
        demand[min_j] -= quantity

    return filled_values

def calculate_final_cost(allocation, costs):
    total_cost = 0
    for i in range(len(allocation)):
        for j in range(len(allocation[i])):
            total_cost += allocation[i][j] * costs[i][j]
    return total_cost

# Interface Streamlit
st.title("Méthode du coût minimal")

# Saisie des données
rows = st.number_input("Donner le nombre des Sources (n)", min_value=1, step=1)
columns = st.number_input("Donner le nombre des Destinations (m)", min_value=1, step=1)

# Entrée de la matrice des coûts
costs_input = st.text_area("Saisissez la matrice des coûts, les valeurs séparées par des espaces, chaque ligne sur une nouvelle ligne.")

if costs_input:
    try:
        # Transformation des entrées en matrice de coûts
        costs = [list(map(int, line.split())) for line in costs_input.splitlines()]
        
        # Vérification des dimensions de la matrice
        if len(costs) != rows or any(len(row) != columns for row in costs):
            st.error(f"La matrice des coûts doit avoir {rows} lignes et {columns} colonnes.")
        else:
            # Saisie des offres et des demandes
            supply = list(map(int, st.text_input("Saisissez les valeurs des offres (séparées par des espaces)").split()))
            demand = list(map(int, st.text_input("Saisissez les valeurs des demandes (séparées par des espaces)").split()))

            if len(supply) != rows or len(demand) != columns:
                st.error(f"Le nombre des offres doit être {rows} et le nombre des demandes doit être {columns}.")
            else:
                # Appeler la méthode du coût minimal
                allocation = least_cost_method(costs, supply[:], demand[:])

                # Affichage des résultats
                st.subheader("Matrice d'allocation :")
                st.write(np.array(allocation))

                final_cost = calculate_final_cost(allocation, costs)
                st.subheader(f"Coût total : {final_cost}")
    except ValueError:
        st.error("Assurez-vous que toutes les valeurs sont numériques et bien formatées.")
