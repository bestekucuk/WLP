import random

# Genetik algoritmanın parametreleri
POPULATION_SIZE = 100  
GENERATION_COUNT = 100  
MUTATION_RATE = 0.1  

def calculate_total_cost(warehouse_file, assigned_depots):
    # Veri dosyasını okuyalım
    with open(warehouse_file, 'r') as file:
        lines = file.readlines()

    depot_count, customer_count = map(int, lines[0].split())

    depots = []
    for line in lines[1:depot_count + 1]:
        capacity, setup_cost = map(float, line.split())
        depots.append((capacity, setup_cost))

    customer_demands = []
    customer_costs = []
    for i in range(customer_count):
        demand = int(lines[depot_count + 1 + i * 2])
        customer_demands.append(demand)
        costs = list(map(float, lines[depot_count + 2 + i * 2].split()))
        customer_costs.append(costs)

    # Toplam maliyeti hesaplayalım
    total_cost = 0
    for i in range(customer_count):
        assigned_depot = assigned_depots[i]
        total_cost += depots[assigned_depot][1]

    return total_cost

def generate_random_solution(depot_count, customer_count):
    return [random.randint(0, depot_count-1) for _ in range(customer_count)]

def crossover(parent1, parent2):
    child = []
    for gene1, gene2 in zip(parent1, parent2):
        # Rastgele bir ebeveynin genini seç
        if random.random() < 0.5:
            child.append(gene1)
        else:
            child.append(gene2)
    return child

def mutate(solution, depot_count):
    mutated_solution = solution.copy()
    for i in range(len(mutated_solution)):
        if random.random() < MUTATION_RATE:
            mutated_solution[i] = random.randint(0, depot_count-1)
    return mutated_solution

def select_parent_index(fitness_scores):
    # Fitness skorlarına dayalı olarak bir ebeveyn seç
    total_fitness = sum(fitness_scores)
    selection_probability = [fitness / total_fitness for fitness in fitness_scores]
    return random.choices(range(len(fitness_scores)), weights=selection_probability)[0]

def genetic_algorithm(warehouse_file):
    # Veri dosyasını okuyalım
    with open(warehouse_file, 'r') as file:
        lines = file.readlines()

    depot_count, customer_count = map(int, lines[0].split())

    # Popülasyonu oluşturalım
    population = [generate_random_solution(depot_count, customer_count) for _ in range(POPULATION_SIZE)]

    # Nesil sayısı kadar evrim yapalım
    for generation in range(GENERATION_COUNT):
        # Fitness skorlarını hesaplayalım
        fitness_scores = [calculate_total_cost(warehouse_file, solution) for solution in population]

        # En iyi çözümü bulalım
        best_solution = population[fitness_scores.index(min(fitness_scores))]

        # Yeni nesil popülasyonu oluşturalım
        new_population = [best_solution]

        # Crossover ve mutasyon uygulayalım
        while len(new_population) < POPULATION_SIZE:
            # Ebeveynleri seçelim
            parent1_index = select_parent_index(fitness_scores)
            parent2_index = select_parent_index(fitness_scores)
            parent1 = population[parent1_index]
            parent2 = population[parent2_index]

            # Crossover işlemini uygulayalım
            child = crossover(parent1, parent2)

            # Mutasyon uygulayalım
            mutated_child = mutate(child, depot_count)

            # Yeni popülasyona ekleme yapalım
            new_population.append(mutated_child)

        # Yeni nesili güncelliyoruz
        population = new_population

    # En iyi çözümü bulalım
    best_solution = population[fitness_scores.index(min(fitness_scores))]

    # Toplam maliyeti hesaplıyoruz
    total_cost = calculate_total_cost(warehouse_file, best_solution)

    return total_cost, best_solution

# Kullanıcıdan hangi dosyanın okunmasını istediğini alalım
print("Kullanılabilir dosya isimleri:")
print("1. wl_16_1.txt")
print("2. wl_200_2.txt")
print("3. wl_500_3.txt")
choice = int(input("Lütfen bir seçenek numarası girin (1, 2 veya 3): "))

# Seçilen dosya ismini belirleyelim
if choice == 1:
    warehouse_file = 'wl_16_1.txt'
elif choice == 2:
    warehouse_file = 'wl_200_2.txt'
elif choice == 3:
    warehouse_file = 'wl_500_3.txt'
else:
    print("Geçersiz seçenek numarası. Program sonlandırılıyor.")
    exit()

# Genetik algoritmayı çalıştıralım
total_cost, assigned_depots = genetic_algorithm(warehouse_file)

# Sonuçları konsola yazdıralım
print("Toplam maliyet:", total_cost)
print("Müşteriye atanan depolar:", " ".join(str(dep) for dep in assigned_depots))
