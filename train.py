import sys,os,neat,pickle
from snake import GAME

def eval_genomes(genomes,config):
    for i, (genome_id,genome) in enumerate(genomes):
        genome.fitness=0
        game=GAME(genome=genome)
        game.train_ai(genome,config)

def run_neat(config,gen=None):
    if gen is None:
        pop=neat.Population(config) #creates the population
        checkpoint_dir=os.path.join(local_dir, "checkpoints")
        if not os.path.exists(checkpoint_dir):
            os.makedirs(checkpoint_dir)
        #this is for printing population results
        checkpoint_prefix = os.path.join(checkpoint_dir, "neat-checkpoint-")
        pop.add_reporter(neat.Checkpointer(1, filename_prefix=checkpoint_prefix))
        pop.add_reporter(neat.StdOutReporter(True))
        stats=neat.StatisticsReporter()
        pop.add_reporter(stats)


        best_neural_network=pop.run(eval_genomes,sys.maxsize) # (function, number of generations)

        with open("best.pickle","wb") as f:
            pickle.dump(best_neural_network,f)
    else:
        pop=neat.Population(config) #creates the population
        checkpoint_dir=os.path.join(local_dir, "checkpoints")
        if not os.path.exists(checkpoint_dir):
            os.makedirs(checkpoint_dir)
        #this is for printing population results
        checkpoint_prefix = os.path.join(checkpoint_dir, "neat-checkpoint-")
        checkpoint_file = os.path.join(checkpoint_dir, "neat-checkpoint-"+str(gen))  # Replace 'x' with the desired generation number
        pop = neat.Checkpointer().restore_checkpoint(checkpoint_file)
        pop.add_reporter(neat.Checkpointer(1, filename_prefix=checkpoint_prefix))
        pop.add_reporter(neat.StdOutReporter(True))
        stats=neat.StatisticsReporter()
        pop.add_reporter(stats)


        best_neural_network=pop.run(eval_genomes,100) # (function, number of generations)
        with open("best.pickle","wb") as f:
            pickle.dump(best_neural_network,f)

def test_winner(config):
    with open("best.pickle","rb") as f:
        winner=pickle.load(f)
    game=GAME(genome=winner,train=False)
    game.test_genome(winner,config)





if __name__=="__main__":
    #gets the necessary configuration variables for neat
    local_dir=os.path.dirname(__file__)
    config_path=os.path.join(local_dir,"config.txt")
    config=neat.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)
    run_neat(config,gen=None) # if you want to test the winning ai, replace this line with test_winner(config)

