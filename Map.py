import time
import numpy as np
import googlemaps
import folium
import random
from geopy.distance import geodesic
import tkinter as tk
from tkinter import Button

# Konum sayısını belirliyoruz
konum_sayisi = 20

shortest_route = []

# Belirli bir aralık içinde rastgele koordinatlar belirliyoruz
min_enlem, max_enlem = 39.57, 40.53
min_boylam, max_boylam = 26.92, 28.51

# Enlem - Boylam
locations = np.random.uniform(low=(min_enlem, min_boylam), high=(max_enlem, max_boylam), size=(konum_sayisi, 2))

location_list = locations.tolist()

renk_kodları = [
    '#ff0000', '#f1000d', '#e4001a', '#d60028', '#c90035',
    '#bb0043', '#ae0050', '#a1005d', '#93006b', '#860078',
    '#780086', '#6b0093', '#5d00a1', '#5000ae', '#4300bb',
    '#3500c9', '#2800d6', '#1a00e4', '#0d00f1', '#0000ff'
]
renk_listesi = []

# Bu renk kodlarını boş bir listeye ekliyoruz
renk_listesi.extend(renk_kodları)

def sürüs_rotaları_cizin(api_key, shortest_route, renk_listesi):
    # Google haritalar Api'ye baglanıyoruz
    gmaps = googlemaps.Client(key=api_key)

    # Burada bir harita oluşturuyoruz
    mymap = folium.Map(location=shortest_route[0], zoom_start=12)

    for i in range(len(shortest_route) - 1):
        origin = shortest_route[i]
        destination = shortest_route[i + 1]
        color_code = renk_listesi[i]

        #  Sürüş yönergelerini alıyoruz
        directions_result = gmaps.directions(origin, destination, mode="driving")
        print(f"{i+1}. rota cizildi")
        time.sleep(30)
        # Rota koordinatlarını çıkarıyoruz burada
        route_coordinates = [(step['start_location']['lat'], step['start_location']['lng']) for step in directions_result[0]['legs'][0]['steps']]
        route_coordinates.append((directions_result[0]['legs'][0]['end_location']['lat'], directions_result[0]['legs'][0]['end_location']['lng']))

        # Rota çizimi
        folium.PolyLine(locations=route_coordinates, color=color_code).add_to(mymap)

    # Haritayı bir HTML dosyasına kaydediyoruz
    mymap.save("araba_rotası.html")

def parents_secim(population, fitness_scores):
    indices = np.argsort(fitness_scores)
    return [population[indices[0]], population[indices[1]]]

def toplam_rota_mesafesi(route):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += np.linalg.norm(locations[route[i]] - locations[route[i + 1]])
    total_distance += np.linalg.norm(locations[route[-1]] - locations[route[0]])  
    return total_distance

def populasyon_olusturma(population_size):
    population = [list(np.random.permutation(konum_sayisi)) for _ in range(population_size)]
    return population

def crossover(parent1, parent2):
    start, end = sorted(random.sample(range(konum_sayisi), 2))
    child = [-1] * konum_sayisi
    child[start:end] = parent1[start:end]
    remaining_values = [value for value in parent2 if value not in child]
    j = 0
    for i in range(konum_sayisi):
        if child[i] == -1:
            child[i] = remaining_values[j]
            j += 1
    return child

def mutation(route):
    index1, index2 = random.sample(range(konum_sayisi), 2)
    route[index1], route[index2] = route[index2], route[index1]
    return route

def mesafe_hesaplama(coord1, coord2):
    return geodesic(coord1, coord2).kilometers

# " Genetik Algoritma "
population_size = 100
generations = 1000

population = populasyon_olusturma(population_size)

for generation in range(generations):
    fitness_scores = [1 / toplam_rota_mesafesi(route) for route in population]

    # parents seçimi
    parents = parents_secim(population, fitness_scores)

    # Çaprazlama işlemi
    child = crossover(parents[0], parents[1])

    # Mutasyon işlemleri
    if random.random() < 0.1:
        child = mutation(child)

    # En az uygunluğa sahip individuali yeni child ile değiştir
    least_fit_index = np.argmin(fitness_scores)
    population[least_fit_index] = child

# En iyi rotayı alıyoruz
best_route = population[np.argmax(fitness_scores)]

# En iyi rotayı ve toplam mesafeyi yazdırıyoruz
print("En iyi rota koordinatları:")
for index in best_route:
    print(locations[index])
    shortest_route.append(locations[index])

print("\nToplam Mesafe:", toplam_rota_mesafesi(best_route))

google_maps_api_key = "Your Google Api Key"

# Sürüş rotalarını çiziyoruz.
sürüs_rotaları_cizin(google_maps_api_key, shortest_route, renk_listesi)

time.sleep(5)

for i in range(len(shortest_route) - 1):
    coord1 = shortest_route[i]
    coord2 = shortest_route[i + 1]
    mesafe = mesafe_hesaplama(coord1, coord2)
    print(f"{coord1} - {coord2} Distance Between Coordinates: {mesafe} km")

class MapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Harita")
        self.root.geometry("1366x768")

        # Left side
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # En iyi rota koordinatları
        self.route_label = tk.Label(self.left_frame, text="En iyi rota koordinatları:")
        self.route_label.pack()

        for index in best_route:
            label_text = f"{locations[index]}"
            label = tk.Label(self.left_frame, text=label_text)
            label.pack()

        # Araya boşluk koyuyoruz
        space_label = tk.Label(self.left_frame, text="")
        space_label.pack(pady=5)

        # Middle section
        self.middle_frame = tk.Frame(self.root)
        self.middle_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Burası mesafelerin görüntüleneceği bölüm
        for i in range(len(best_route) - 1):
            coord1 = locations[best_route[i]]
            coord2 = locations[best_route[i + 1]]
            mesafe = mesafe_hesaplama(coord1, coord2)
            distance_label_text =f"{coord1} - {coord2} Koordinatları Arasındaki Mesafe: {mesafe} km"

            distance_label = tk.Label(self.middle_frame, text=distance_label_text)
            distance_label.pack()

        # Right side
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10)


        # Button
        self.show_route_button = Button(self.right_frame, text="Güzergahı_göster", command=self.show_route)
        self.show_route_button.pack()

    def show_route(self):
        # "Güzergahı_göster" butonu tıklandığında yapılacak işlemler
        import webbrowser

        # Burada HTML dosyasını açıyoruz
        webbrowser.open("araba_rotası.html")

# Burada uygulamayı oluşturuyoruz
root = tk.Tk()
app = MapApp(root)
root.mainloop()
